from langgraph.graph import StateGraph,START,END
from app.utils.state import AgentState
from app.utils.nodes import *

builder = StateGraph(AgentState)

builder.add_node("input_handler",input_handler)
builder.add_node("memory_updater",memory_updater)
builder.add_node("responder",responder)
builder.add_node("summarizer",summarizer)
builder.add_edge(START,"input_handler")
builder.add_edge("input_handler","memory_updater")
builder.add_edge("memory_updater","responder")
builder.add_conditional_edges("responder",route_after_responder,{"END":END , "summarizer":"summarizer"})
builder.add_edge("summarizer",END)

chat_agent = builder.compile()
