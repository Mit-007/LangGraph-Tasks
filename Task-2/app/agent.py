from langgraph.graph import StateGraph, START ,END
from app.utils.state import AgentState
from app.utils.nodes import *
from langgraph.checkpoint.memory import InMemorySaver


# bulid Graph :
builder = StateGraph(AgentState)
builder.add_node("call_llm",call_llm)
builder.add_node("tool_node",tool_node)
builder.add_edge(START,"call_llm")
builder.add_conditional_edges("call_llm",route_tool_node,{"tool_node":"tool_node" , "END" : END})
builder.add_edge("tool_node","call_llm")
builder.add_edge("call_llm",END)

agent = builder.compile(checkpointer=InMemorySaver())

