from app.utils.state.state_DB_researcher import *
from app.services.call_llm import llm_DB_researcher as llm
from langgraph.types import Send
from app.services.logger import logger
import sqlite3

# ============
# get_schema_list
# ============
def get_schema_list(state: DB_researcher_State) -> DB_researcher_State:
    logger.info("DB_researcher:-get_schema_list")

    try:
        conn = sqlite3.connect(state["db_path"])
        cursor = conn.cursor()

        cursor.execute("""
            SELECT sql
            FROM sqlite_master
            WHERE type='table'
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)

        schema = "\n\n".join(
            row[0] for row in cursor.fetchall()
        )

        conn.close()

        return {
            "schema_of_collection": schema
        }

    except Exception as e:
        logger.error(f"Error in get_schema_list: {e}")
        return {}
    
    finally:
        if conn:
            conn.close()



# ============
# orchestator_DB_researcher
# ============
def orchestator_DB_researcher(state: DB_researcher_State) -> DB_researcher_State:
    logger.info("DB_researcher:-orchestrator")

    try:

        if not state.get("schema_of_collection"):
            raise ValueError("schema_of_collection is empty")

        prompt_orchestator_DB_researcher = f"""
        You are an expert SQLite Query Planning Agent.

        You will receive:

        1. Database Schema
        2. User Question

        Your task is to analyze the question and generate the SQLite query or queries required to answer it.

        DATABASE SCHEMA:
        {state['schema_of_collection']}

        USER QUESTION:
        {state['query']}

        Instructions:

        1. Carefully understand the user's intent.

        2. Use ONLY tables and columns that exist in the provided schema.

        3. Generate valid SQLite SQL.

        4. If the question can be answered with a single query,
        return exactly one query.

        5. If the question requires multiple steps,
        generate multiple queries in execution order.

        6. Prefer a single SQL query with JOINs and aggregations whenever possible.

        7. Never invent tables, columns, relationships, or values.

        8. Use explicit JOIN conditions.

        9. Use aggregate functions when required:
        - COUNT
        - SUM
        - AVG
        - MAX
        - MIN

        10. For ranking requests:
            use ORDER BY and LIMIT.

        11. For date filtering:
            use SQLite-compatible date syntax.

        12. Return ONLY the queries.
            Do not explain them.

        13. If the question cannot be answered using the schema,
            return an empty list.

        Output Format:

        [
            {{
                "query_name": "short_descriptive_name",
                "query": "SQL_QUERY_HERE"
            }}
        ]
        """

        structured_llm = llm.with_structured_output(DB_researcher_llm_schema)
        result = structured_llm.invoke(prompt_orchestator_DB_researcher)

        return {
            "sub_querys": result.sub_querys
        }

    except Exception as e:
        logger.error(f"Error in orchestator_DB_researcher: {e}")
        return {
            "sub_querys": []
        }



# ============
# route_DB_researcher_worker
# ============
def route_DB_researcher_worker(state: DB_researcher_State):
    logger.info("DB_researcher:-route function")

    try:
        sub_querys = state.get("sub_querys", [])

        if not sub_querys:
            logger.warning("No sub_querys found")
            return []

        return [
            Send(
                "worker_DB_researcher",
                {
                    "sub_query": sub_query,
                    "db_path": state["db_path"]
                }
            )
            for sub_query in sub_querys
        ]

    except Exception as e:
        logger.error(f"Error in route_DB_researcher_worker: {e}")
        return []


# ============
# worker_DB_researcher
# ============
def worker_DB_researcher(state: DB_researcher_worker_State) -> DB_researcher_State:
    logger.info("DB_researcher:-worker")

    conn = None

    try:
        conn = sqlite3.connect(state["db_path"])
        cursor = conn.cursor()

        cursor.execute(state["sub_query"].query)
        res = cursor.fetchall()

        state["result"] = res

    except Exception as e:
        logger.exception(f"Error in worker_DB_researcher: {e}")

        state["result"] = f"Exception: {str(e)}"

    finally:
        if conn:
            conn.close()

    return {
        "workers_output": [state]
    }



# ============
# aggregater_DB_researcher
# ============
def aggregater_DB_researcher(state: DB_researcher_State) -> DB_researcher_State:
    logger.info("DB_researcher:-aggregator Node")

    try:
        workers_output = state.get("workers_output", [])

        if not workers_output:
            logger.warning("No workers_output found")

            return {
                "final_result": "Unable to answer the question because no data was retrieved."
            }

        final_report_prompt = f"""
        You are a Database Research Report Generator.

        You will be given:

        1. The user's original question.
        2. Results collected from one or more database researcher workers.

        USER QUESTION:
        {state['query']}

        WORKER OUTPUTS:
        {workers_output}

        Instructions:

        1. Carefully review every worker output.

        2. Combine information from all workers before answering.

        3. Focus on answering the user's question, not on explaining SQL queries.

        4. Use the query results as evidence for your answer.

        5. If multiple worker outputs contribute to the answer,
        synthesize them into a single coherent response.

        6. If a worker output is empty, mention that no matching data
        was found if relevant.

        7. If the data is insufficient to answer the question completely,
        clearly state what information is available and what is missing.

        8. Do not invent facts that are not present in the worker outputs.

        9. Do not mention internal implementation details.

        10. Present numerical values exactly as provided.

        11. Use concise but informative language.

        12. When useful, provide:
            - bullet points
            - rankings
            - summaries
            - comparisons

        13. If the user asks for analysis, provide analysis based only
        on the available data.

        Generate the final report now.
        """

        structured_llm = llm.with_structured_output(
            DB_researcher_aggregator_schema
        )

        result = structured_llm.invoke(final_report_prompt)

        return {
            "final_result": result.final_answer
        }

    except Exception as e:
        logger.error(f"Error in aggregater_DB_researcher: {e}")

        return {
            "final_result": f"Exception occurred while generating the final report: {str(e)}"
        }