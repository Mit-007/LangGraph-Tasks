from app.utils.state.state_Doc_researcher import *
from app.services.call_llm import llm_Doc_researcher as llm
from app.services.call_llm import embedding_model
from langgraph.types import Send
from langchain_pinecone import PineconeVectorStore
from app.services.logger import logger
from app.core.config import INDEX_NAME


# ============
# orchestator_Doc_researcher
# ============
def orchestator_Doc_researcher(state: Doc_researcher_State) -> Doc_researcher_State:
    logger.info("Doc_researcher:-orchestrator")
    try:
        topic = state.get("topic")

        if not topic or not topic.strip():
            raise ValueError("topic is empty")

        prompt_orchestator_Doc_researcher = f"""
        You are a RAG Query Planning Agent.

        Research Topic:
        {topic}

        Your task is to generate semantic retrieval queries for a document database.

        Instructions:

        - Create queries that maximize retrieval of relevant document chunks.
        - Use natural language.
        - Prefer question-style queries.
        - Cover the essential aspects of the topic.
        - Avoid overlap.
        - Generate only the minimum number of queries needed.
        - maximum you create 5 sun query.
        - if not need more sub query divison then try to avoid it.

        Return only a Python list of strings.
        """

        structured_llm = llm.with_structured_output(Doc_researcher_llm_sceama)

        result = structured_llm.invoke(prompt_orchestator_Doc_researcher)

        return {
            "sub_querys": result.sub_querys
        }

    except Exception as e:
        logger.error(
            f"Error in orchestator_Doc_researcher: {e}"
        )

        return {
            "sub_querys": []
        }
    

# ============
# route_Doc_researcher_worker
# ============    
def route_Doc_researcher_worker(state: Doc_researcher_State):
    logger.info("Doc_researcher:-route function")

    try:
        sub_querys = state.get("sub_querys")

        if not isinstance(sub_querys, list):
            raise ValueError("sub_querys must be a list")

        if len(sub_querys) == 0:
            raise ValueError("sub_querys is empty")

        return [
            Send(
                "worker_Doc_researcher",
                {
                    "sub_query": sub_query
                }
            )
            for sub_query in sub_querys
        ]

    except Exception as e:
        logger.error(
            f"Error in route_Doc_researcher_worker: {e}"
        )
        return []



# ============
# worker_Doc_researcher
# ============
def worker_Doc_researcher(state: Doc_researcher_worker_State) -> Doc_researcher_State:
    logger.info("Doc_researcher:-worker")
    try:
        sub_query = state.get("sub_query")
        if not sub_query:
            raise ValueError("sub_query is empty")

        vectorstore = PineconeVectorStore(
            index_name=INDEX_NAME,
            embedding=embedding_model
        )

        results = vectorstore.similarity_search(sub_query,k=1)

        context = "\n\n".join(
            doc.page_content for doc in results
        )

        worker_result = {
            "sub_topic": sub_query,
            "result": context
        }

    except Exception as e:
        logger.error(f"Error in worker_Doc_researcher: {e}")

        worker_result = {
            "sub_topic": state.get("sub_query"),
            "result": str(e)
        }

    return {
        "workers_output": [worker_result]
    }


# ============
# aggregater_Doc_researcher
# ============
def aggregater_Doc_researcher(state: Doc_researcher_State) -> Doc_researcher_State:
    logger.info("Doc_researcher:-aggregator Node")
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

        structured_llm = llm.with_structured_output(Doc_researcher_aggregator_sceama)

        result = structured_llm.invoke(final_report_prompt)

        return {
            "final_result": result.final_report
        }

    except Exception as e:
        logger.error(
            f"Error in aggregater_Doc_researcher: {e}"
        )

        return {
            "final_result": f"Exception: {str(e)}"
        }