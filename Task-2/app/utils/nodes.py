from app.utils.state import AgentState,LLMResponse
from app.utils.tool import calculator,python_repl,web_search
from langgraph.types import interrupt
from typing import Literal
from app.services.prompt import llm_prompt
from app.services.llm_service import llm
from app.services.logger import logger
from app.core.constant import MAX_ITERATION

# ===========
# call_llm
# ===========
def call_llm(state: AgentState) -> AgentState:
    logger.info("Node:-call_llm")
    try:

        if state["question"].strip =="":
            raise ValueError("Invalid Input , question is empty")

        structured_llm_prompt = llm_prompt(
            state["question"],
            state["tool_call_log"],
            state["iteration_count"]
        )

        if not llm:
            raise ValueError("LLM service is not available.")

        structured_llm = llm.with_structured_output(LLMResponse)

        result = structured_llm.invoke(structured_llm_prompt)

        if result.tool_args is None:
            tool_args_dict = None
        else:
            tool_args_dict = result.tool_args.model_dump()

        return {
            "final_answer": result.final_answer,
            "tool_call": result.tool_call,
            "through": result.through,
            "tool_name": result.tool_name,
            "tool_args": tool_args_dict
        }

    except Exception as e:
        logger.error(f"Error in call_llm: {e}")

        return {
            "final_answer": f"Error while processing request: {str(e)}",
            "tool_call": False,
            "through": "",
            "tool_name": None,
            "tool_args": None
        }


# ===========
# route_tool_node
# ===========
def route_tool_node(state: AgentState) -> Literal["tool_node", "END"]:
    logger.info("Node:-route_tool_node")
    try:
        if state["tool_call"] and state['iteration_count'] < MAX_ITERATION:
            return "tool_node"
        else :
            return "END"

    except Exception as e:
        logger.exception(f"Error in route_tool_node: {e}")
        return "END"


# ===========
# tool_node
# ===========
def tool_node(state : AgentState):
    logger.info("Node:-tool_node")

    tool_name = state['tool_name']
    tool_answer = None

    if tool_name=='calculator':
        approval = interrupt("can i use a calculator tool (yes/no)")

        if approval.lower() == "yes": 
            tool_answer = calculator.invoke(state['tool_args'] )

        else : tool_answer="not approval for use calculator tool"



    if tool_name=='web_search':

        approval = interrupt("can i use a web search tool (yes/no)")

        if approval.lower() == "yes": 
            tool_answer = web_search.invoke(state['tool_args'])

        else : tool_answer="not approval for use web_search tool"

        
        

    if tool_name =='python_repl':

        approval = interrupt("can i use a python_repl tool (yes/no)")

        if approval.lower() == "yes": 
            tool_answer = python_repl.invoke(state['tool_args'])

        else : tool_answer="not approval for use pyhton_repl tool"
    

    try:
        tool_dict = {
            "tool_name":tool_name,
            "tool_args":state['tool_args'],
            "tool_answer":tool_answer
        }

        state['tool_call_log'].append(tool_dict)

        return {
            'tool_call_log':state["tool_call_log"],
            'iteration_count': state['iteration_count'] + 1,
            'tool_result':tool_answer
        }
    
    except Exception as e:
        logger.exception(f"Error in tool_node: {e}")

        error_message = f"Tool execution failed: {str(e)}"

        tool_dict = {
            "tool_name": state.get("tool_name"),
            "tool_args": state.get("tool_args"),
            "tool_answer": error_message,
        }

        state["tool_call_log"].append(tool_dict)

        return {
            "tool_call_log": state["tool_call_log"],
            "iteration_count": state.get("iteration_count", 0) + 1,
            "tool_result": error_message,
        }