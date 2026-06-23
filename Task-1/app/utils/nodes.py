from app.utils.state import *
from app.utils.call_llm import call_llm
from app.utils.logger import logger
from app.core.constant import *

# ==========
# input_handler
# ==========
def input_handler(state : AgentState)->AgentState:
    """Check whether the input is empty."""
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

        # --> if Input is not valid , then current turn is not count !
        return {
            "messages": state["messages"],
            "turn_count": state["turn_count"],
        }


# ==========
# memory_updater
# ==========
def memory_updater(state: AgentState) -> AgentState:
    """Optimize memory after the summary and mood counter reach their configured limits."""
    try:

        message_list = state["messages"]
        mood_list = state["mood"]
        new_summary_status = state['summary_status']
        
        # -----> memory menagement after summary :

        if state["turn_count"] % SUMMARY_COUNTER == 1 or SUMMARY_COUNTER==1:
            # =============
            #  if some reasone summary not generated then skip the remove message step, till next summary not generated 
            # ============
            if state['summary_status'] == True :
                message_list = state["messages"][-1:]
                new_summary_status = False


        # -----> memory menagement after reach Mood counter limit :
        if state["turn_count"] % MOOD_HISTORY_COUNTER  == 1 or MOOD_HISTORY_COUNTER == 1:
                mood_list = []

        return {
            "messages": message_list,
            "mood": mood_list,
            'summary_status' : new_summary_status
        }

    except Exception as e:
        logger.error(f"Error in memory_updater: {e}")
        return {}


# ==========
# responder
# ==========
def responder(state: AgentState) -> AgentState:
    """Generate the user response using the LLM."""
    try:
        if (
            not state.get("messages")
            or not state["messages"][-1]
        ):
            raise ValueError("Last message is empty. Cannot generate response.")

        llm = call_llm()

        if not llm:
            raise ValueError("LLM service is not available.")

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

        Response Style: * If the mood is Positive, begin with a brief cheerful or appreciative acknowledgement, then answer the question. 
        * If the mood is Negative, begin with a brief empathetic or encouraging sentence, then answer the question. 
        * If the mood is Neutral, answer the question naturally and directly. 
        * Keep the acknowledgement or encouragement short and ensure the main focus remains the answer.
        """

        structured_llm = llm.with_structured_output(ouput_schema)
        response = structured_llm.invoke(prompt)

        answer = str(response.output.content)

        state["messages"].append(answer)
        state["mood"].append(response.mood)

        return {
            "messages": state["messages"],
            "mood": state["mood"]
        }

    except Exception as e:
        logger.error(f"Error in responder: {e}")

        # append error message for output refrences
        state['messages'].append("error occurred")

        return {
            "messages": state["messages"],
            "mood": state["mood"]
        }


# ==========
# route_after_Responder
# ==========
def route_after_responder(state:AgentState)->Literal["responder","summarizer"]:
    """Route to the first summary node if the current turn value matches the summary counter."""
    try:
        message = state["messages"][-1].strip()

        if not message:
            raise ValueError("Message cannot be empty")
        
        elif state['turn_count'] % SUMMARY_COUNTER == 0:
            return "summarizer"
        
        else :
            return "END"
        
    except Exception as e:
        logger.error(f"{e}")
        return 'END'


# ==========
# summarizer
# ==========
def summarizer(state: AgentState) -> AgentState:
    """Generate a summary of past conversations."""
    try:
        if (not state.get("messages")or not state["messages"][-1]):
            raise ValueError(
                "given message is empty."
            )
        
        llm = call_llm()

        if not llm:
            raise ValueError("LLM service is not available.")

        messages_for_summary = state["messages"]

        structured_llm = llm.with_structured_output(summary_schema)

        if state["summary"] == "":
            prompt = f"""
            You are a conversation summarization assistant responsible for maintaining long-term memory.
            Your task is to generate a concise yet comprehensive summary of the conversation.

            Instructions:
            - Preserve all important facts, decisions, preferences, goals, and context that may be useful in future conversations.
            - Do not omit any critical information that could affect future responses.
            - Remove redundant or repetitive details.
            - Organize the summary logically and clearly.
            - Keep the summary as concise as possible while retaining all essential information.

            Conversation:
            {messages_for_summary}
            """
        else:
            prompt = f"""
            You are a conversation summarization assistant responsible for maintaining long-term memory. 
            You are given an existing summary and some new conversation messages. 
            Update the summary by incorporating any new important information. 
            
            Instructions: 
            - Preserve all important facts from the previous summary. 
            - Add new preferences, goals, decisions, tasks, and context. 
            - Remove duplicated information. - Keep the summary well organized. 
            - Do not invent information. 
            - Keep the summary compact while preserving every important detail.

            Previous Summary:
            {state['summary']}

            Recent Messages:
            {messages_for_summary}
            """

        response = structured_llm.invoke(prompt)

        answer = str(response.summary)

        return {
            "summary": answer,
            "messages": state["messages"],
            'summary_status' : True
        }

    except Exception as e:
        logger.error(f"Error in summarizer: {e}")

        return {
            "summary": state["summary"],
            "messages": state["messages"],
            "summary_status" :False
        }
