from langgraph.types import Send
from app.utils.state.states import *
from app.services.call_llm import llm as get_llm
from app.utils.subgraph.graph_DB_researcher import DB_researcher_agent
from app.utils.subgraph.graph_doc_researcher import Doc_researcher_agent
from app.utils.subgraph.graph_web_researcher import web_researcher_agent
from app.services.logger import logger
from app.core.config import DB_PATH_OF_COLLECTION

# ==============
# orchestator
# ============
def orchestator(state: MainState) -> MainState:
    """Generate sub-queries from the input query for worker nodes."""
    logger.info("Node:-orchestator Node")

    try:
        orchestator_llm_prompt = f"""
        You are a Research Orchestrator.

        Your job is to analyze the user's request and create a research plan.

        You have access to the following researcher agents:

        1. DB_researcher_agent
        Purpose:
        - Structured company data
        - SQL databases
        - Sales data
        - Customers
        - Employees
        - Products
        - Inventory
        - Transactions
        - Payments
        - Analytics
        - Operational metrics

        2. Doc_researcher_agent
        Purpose:
        - PDFs
        - Reports
        - Policies
        - Contracts
        - Manuals
        - Presentations
        - Meeting notes
        - Internal documentation
        - Knowledge base content

        3. web_researcher_agent
        Purpose:
        - Internet research
        - Current events
        - News
        - Regulations
        - Competitor information
        - Public company information
        - Market trends
        - Research papers
        - Recent developments

        Your task:

        1. Analyze the user's question.
        2. Determine which researchers are required.
        3. If multiple pieces of information are needed from the same researcher,
           combine them into a single research query.
        4. The query should clearly describe the information that researcher must gather.
        5. If a question requires information from multiple sources,
           create one task for each relevant researcher.
        6. Do not create duplicate tasks for the same researcher.
        7. Do not assign work to researchers that are not needed.
        8. Focus on information gathering, not final answer generation.
        9. The query should preserve all details relevant to that researcher.

        Examples:

        User:
        "Which employee generated the highest sales revenue and what are the latest industry trends affecting that product category?"

        Output:
        [
            {{
                "researcher_name": "DB_researcher_agent",
                "query": "Find the employee with the highest sales revenue and identify the product category responsible for that revenue."
            }},
            {{
                "researcher_name": "web_researcher_agent",
                "query": "Research the latest industry trends affecting the identified product category."
            }}
        ]

        Return only the structured output.

        User Question:
        {state['user_input']}
        """

        llm = get_llm()

        if not llm:
            raise ValueError("LLM service is not available.")

        structured_llm = llm.with_structured_output(orchestator_llm_schema)
        result = structured_llm.invoke(orchestator_llm_prompt)

        return {
            'researchers_list': result.researchers_list
        }

    except Exception as e:
        logger.error(f"Error in orchestator node: {e}")

        return {
            'researchers_list': []
        }



# ==============
# route_workers
# ============
from langgraph.types import Send

def route_workers(state: MainState):
    """Route to a worker node using the send() API."""
    logger.info("Node:-route_workers")

    try:
        tasks = state.get("researchers_list", [])

        if not tasks:
            logger.warning("No researchers found to route")
            return []

        return [
            Send(
                "worker",
                {
                    "researcher_name": task["researcher_name"],
                    "query": task["query"]
                }
            )
            for task in tasks
        ]

    except Exception as e:
        logger.error(f"Error in route_workers: {e}")
        return []



# ==============
# worker
# ============
def worker(state: WorkerState) -> MainState:
    """Execute the given task and generate the output."""
    try:
        researcher_name = state["researcher_name"]
        logger.info(f"🧠 Start Researcher : {researcher_name}")

        response = None

        if researcher_name == 'DB_researcher_agent':
            
            if not DB_PATH_OF_COLLECTION:
                raise ValueError("DB_PATH_OF_COLLECTION_TASK_3 is missing. Please set it in your .env file.")
            
            input_state = {
                "query": state['query'],
                "db_path": DB_PATH_OF_COLLECTION,
                "sub_querys": [],
                "schema_of_collection": {},
                "workers_output": [],
                "final_result": ""
            }
            response = DB_researcher_agent.invoke(input_state)

        elif researcher_name == 'Doc_researcher_agent':
            input_state = {
                'topic': state['query'],
                'sub_querys': [],
                'workers_output': [],
                'final_report': ""
            }
            response = Doc_researcher_agent.invoke(input_state)

        else:
            input_state = {
                'topic': state["query"],
                'sub_topics': [],
                'workers_output': [],
                'final_result': ""
            }
            response = web_researcher_agent.invoke(input_state)

        logger.info(f"🧠 End Researcher : {researcher_name}")

        return {
            "researchers_output": [
                f"Researcher : {researcher_name}, query : {state['query']} , result: {response.get('final_result', response)}"
            ]
        }

    except Exception as e:
        logger.error(f"Error in worker for {state.get('researcher_name', 'UNKNOWN')}: {e}")

        return {
            "researchers_output": [
                f"Researcher : {state.get('researcher_name','UNKNOWN')}, query : {state.get('query','')}, result: ERROR"
            ]
        }


# ==============
# aggregater
# ============
def aggregater(state: MainState) -> MainState:
    """Combine the outputs from all worker nodes."""
    logger.info("aggregator Node")
    try:
        report_aggregater_prompt = f"""
        You are a Senior Research Analyst.

        You will receive:

        1. The original user question.
        2. Research results collected from multiple sources.

        The research results may come from:
        - Databases
        - Documents
        - Web research

        Each research result contains:

        {{
            "sub_query": "...",
            "result": "..."
        }}

        The sub_query explains what information was investigated.
        The result contains the findings.

        ----------------------------------------
        USER QUESTION
        ----------------------------------------

        {state.get('user_input', '')}

        ----------------------------------------
        RESEARCH RESULTS
        ----------------------------------------

        {state.get('researchers_output', [])}

        ----------------------------------------
        YOUR TASK
        ----------------------------------------

        Create a complete and accurate answer to the user's question.

        Instructions:

        1. Read every research result carefully.
        2. Use ALL relevant findings.
        3. Combine information from different sources into a single coherent report.
        4. If multiple results discuss the same topic, merge them naturally.
        5. Focus on answering the user's question directly.
        6. Never mention:
           - researcher agents
           - databases
           - SQL
           - tools
           - internal workflows
           - sub_query values
        7. If the question asks for comparison, compare the relevant findings.
        8. If some information is unavailable, clearly state what is known and what could not be determined.
        9. Use only information present in the provided research results.
        10. Prefer a professional report style.
        11. Use headings and bullet points when helpful.
        12. Provide a detailed report for complex questions.

        ----------------------------------------
        OUTPUT
        ----------------------------------------

        Return only the final report as string,
        """

        llm = get_llm()

        if not llm:
            raise ValueError("LLM service is not available.")

        structured_llm = llm.with_structured_output(aggregator_llm_schema)
        result = structured_llm.invoke(report_aggregater_prompt)

        return {
            "final_report": result.final_answer
        }

    except Exception as e:
        logger.exception(f"Error in aggregator node: {e}")

        return {
            "final_report": "Error: Unable to generate final report due to internal failure."
        }