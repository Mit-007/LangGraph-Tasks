from tavily import TavilyClient
from app.utils.state.state_web_researcher import *
from app.services.call_llm import llm_web_researcher
from langgraph.types import Send
from app.services.logger import logger
from app.core.config import TAVILY_API_KEY
from app.core.constant import MAX_RESULTS_WEB_SEARCH
# ===========
# orchestator_web_researcher
# ===========
def orchestator_web_researcher(state: web_researcher_State) -> web_researcher_State:
    """Generate sub-queries from the input query for worker nodes."""
    logger.info("web_researcher:-orchestrator Node")

    try:
        topic = state.get("topic")

        if not topic or not topic.strip():
            raise ValueError("topic is empty")

        prompt = f"""
        You are a Web Research Planning Agent.

        Your task is to prepare a small set of focused web-search topics.

        Research Topic:
        {topic}

        Instructions:

        1. Analyze the topic.
        2. Identify only the essential areas that must be researched.
        3. Do NOT create unnecessary or overly detailed sub-topics.
        4. Create sub-topics depending on topic complexity.
        5. Each sub-topic should be independently searchable on the web.
        6. Avoid overlap between sub-topics.

        Return:

        Only return the topic and sub-topic list.
        """

        llm = llm_web_researcher()

        if not llm:
            raise ValueError("LLM service is not available.")

        structured_llm = llm.with_structured_output(
            web_researcher_llm_sceama
        )

        result = structured_llm.invoke(prompt)

        return {
            "sub_topics": result.sub_topic
        }

    except Exception as e:
        logger.error(
            f"Error in orchestator_web_researcher: {e}"
        )

        return {
            "sub_topics": []
        }

# ===========
# route_web_researcher_worker
# ===========
def route_web_researcher_worker(state: web_researcher_State):
    """Route to a worker node using the send() API."""
    logger.info("web_researcher:-route function")

    try:
        sub_topics = state.get("sub_topics", [])

        if not sub_topics:
            logger.warning("No sub_topics found")
            return []

        return [
            Send(
                "worker_web_researcher",
                {
                    "sub_topic": sub_topic
                }
            )
            for sub_topic in sub_topics
        ]

    except Exception as e:
        logger.error(f"Error in route_web_researcher_worker: {e}")
        return []



# ===========
# worker_web_researcher
# ===========
def worker_web_researcher(state: web_researcher_worker_State) -> web_researcher_State:
    """Execute the given task and generate the output."""
    logger.info("web_researcher:-worker Node")

    try:
        sub_topic = state.get("sub_topic")

        if not sub_topic:
            raise ValueError("sub_topic is empty")
        
        if not TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY is missing. Please set it in your .env file.")

        client = TavilyClient(TAVILY_API_KEY)

        response = client.search(
            query=sub_topic,
            search_depth="basic",
            max_results=MAX_RESULTS_WEB_SEARCH
        )

        worker_result = {
            "sub_topic": sub_topic,
            "result": response
        }

    except Exception as e:
        logger.error(f"Error in worker_web_researcher: {e}")

        worker_result = {
            "sub_topic": state.get("sub_topic"),
            "result": str(e)
        }

    return {
        "workers_output": [worker_result]
    }


# ===========
# aggregater_web_researcher
# ===========
def aggregater_web_researcher(state: web_researcher_State) -> web_researcher_State:
    """Combine the outputs from all worker nodes."""
    logger.info("web_researcher:-aggregator Node")

    try:
        workers_output = state.get("workers_output")

        if not workers_output:
            raise ValueError("workers_output is empty")

        final_report_prompt = f"""
        You are a Research Report Generator.

        Topic:
        {state['topic']}

        Collected Research:
        {workers_output}

        Instructions:

        1. Read all research results carefully.
        2. Combine related information from different research results.
        3. Remove duplicate or repetitive content.
        4. Keep only information that is relevant to the research topic.
        5. Ignore unrelated or low-quality information.
        6. Do NOT add facts from your own knowledge.
        7. Do NOT make assumptions or invent information.
        8. If two results discuss the same point, merge them into a single concise explanation.
        9. Organize the report into logical sections based on the collected information.
        10. Maintain a clear and professional writing style.
        11. Preserve important facts, statistics, findings, and conclusions from the research results.
        12. The report should be comprehensive but concise.
        13. If information is missing for a section, do not create content for it.

        Output Requirements:

        - Generate a single coherent report.
        - Use section headings when appropriate.
        - Ensure smooth flow between sections.
        - Include a brief conclusion summarizing the key findings.
        - Return ONLY the final report text.
        """

        llm = llm_web_researcher()

        if not llm:
            raise ValueError("LLM service is not available.")

        structured_llm = llm.with_structured_output(
            web_researcher_aggregator_sceama
        )

        result = structured_llm.invoke(final_report_prompt)

        return {
            "final_result": result.final_answer
        }

    except Exception as e:
        logger.error(f"Error in aggregater_web_researcher: {e}")

        return {
            "final_result": f"Exception: {str(e)}"
        }