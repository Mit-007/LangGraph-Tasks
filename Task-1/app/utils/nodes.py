from app.utils.state import *
from app.utils.call_llm import call_llm

# =============
# logger SetUp
# =============
import logging

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

def input_handler(state : AgentState)->AgentState:
    try:
        message = state["messages"][-1].strip()

        if not message:
            raise ValueError("Message cannot be empty")

        state["messages"][-1] = message

        return {
            "messages": state["messages"],
            "turn_count": state["turn_count"] + 1,
        }

    except Exception as e:
        logger.error(f"{e}")
        state["messages"][-1] = ""

        return {
            "messages": state["messages"],
            "turn_count": state["turn_count"],
        }


def route_after_input_handler(state:AgentState)->Literal["responder","summarizer"]:
    if state['turn_count'] % 5 == 1  and state['turn_count']!= 1:
        return "summarizer"
    else :
        return "responder"


def responder(state: AgentState) -> AgentState:
    try:
        if (
            not state.get("messages")
            or not state["messages"][-1]
        ):
            raise ValueError(
                "Last message is empty. Cannot generate response."
            )

        llm = call_llm()

        prompt = f"""
        You are a helpful AI assistant.

        Conversation Summary (all past conversation compressed):
        {state['summary']}

        Recent Messages (not yet included in the summary):
        {state['messages']}

        Current Question:
        {state['messages'][-1]}

        Instructions:
        * Use BOTH the conversation summary and the recent messages as context.
        * The summary contains older conversation history.
        * The recent messages contain the latest conversation that has not yet been summarized.
        * Answer the current question using all available context and your own knowledge when needed.
        * Do not repeat the summary unless it is relevant to the answer.

        Mood Classification:
        * Determine the user's mood from the current question only.
        * Classify the mood as exactly one of:
        - Positive: happiness, excitement, gratitude, confidence, optimism.
        - Neutral: factual questions, requests for information, or unclear emotion.
        - Negative: sadness, frustration, anger, stress, anxiety, disappointment, complaints.
        * If the mood is unclear, choose "neutral".
        """

        structured_llm = llm.with_structured_output(ouput_schema)
        response = structured_llm.invoke(prompt)

        answer = str(response.output.content)

        state["messages"].append(answer)
        state["mood"].append(response.mood)

        return {
            "messages": state["messages"],
            "mood": state["mood"],
        }

    except Exception as e:
        logger.exception(f"Error in responder: {e}")

        return {
            "messages": state["messages"],
            "mood": state["mood"],
        }


def summarizer(state: AgentState) -> AgentState:
    try:
        if (
            not state.get("messages")
            or not state["messages"][-1]
        ):
            raise ValueError(
                "Last message is empty. Cannot generate response."
            )

        llm = call_llm()

        last_message = state["messages"].pop()

        structured_llm = llm.with_structured_output(summary_schema)

        if state["summary"] == "":
            prompt = f"""
            You are a conversation summarization assistant.

            Your task is to create a chat summary.

            Instructions:
            Generate as much as Small And usable summary.

            Recent Messages:
            {state['messages']}
            """
        else:
            prompt = f"""
            You are a conversation summarization assistant.

            Your task is to create an updated chat summary by combining:

            1. The existing conversation summary.
            2. The most recent chat messages.

            Instructions:
            Generate as much as Small And usable summary.

            Previous Summary:
            {state['summary']}

            Recent Messages:
            {state['messages']}
            """

        response = structured_llm.invoke(prompt)

        answer = str(response.summary)

        state["messages"].append(last_message)

        return {
            "summary": answer,
            "messages": state["messages"],
        }

    except Exception as e:
        logger.exception(f"Error in summarizer: {e}")

        return {
            "summary": state["summary"],
            "messages": state["messages"],
        }
    
def memory_updater(state: AgentState) -> AgentState:
    try:
        if not state["messages"][-1]:
            state["messages"].pop()
            return {
                "messages": state["messages"]
            }

        if state["turn_count"] == 1 or state["turn_count"] % 5 != 1:
            return {}

        message_list = state["messages"][-2:]

        if state["turn_count"] % 10 == 1:
            return {
                "messages": message_list,
                "mood": []
            }

        if state["turn_count"] % 5 == 1:
            return {
                "messages": message_list
            }

        return {}

    except Exception as e:
        logger.exception(f"Error in memory_updater: {e}")

        return {}

    