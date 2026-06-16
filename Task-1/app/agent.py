from langgraph.graph import StateGraph,START,END
from app.utils.state import *
from app.utils.nodes import *

builder = StateGraph(AgentState)

builder.add_node("input_handler",input_handler)
builder.add_node("memory_updater",memory_updater)
builder.add_node("responder",responder)
builder.add_node("summarizer",summarizer)
builder.add_edge(START,"input_handler")
builder.add_conditional_edges("input_handler",route_after_input_handler,{"responder":"responder" , "summarizer":"summarizer"})
builder.add_edge("summarizer","responder")
builder.add_edge("responder","memory_updater")
builder.add_edge("memory_updater",END)

chat_agent = builder.compile()
