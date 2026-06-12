from langgraph.graph import StateGraph,START ,END
from app.utils.state.state_web_researcher import web_researcher_State
from app.utils.nodes.nodes_web_researcher import *
from langgraph.checkpoint.memory import InMemorySaver

builder = StateGraph(web_researcher_State)

builder.add_node("orchestator_web_researcher",orchestator_web_researcher)
builder.add_node("worker_web_researcher",worker_web_researcher)
builder.add_node("aggregater_web_researcher",aggregater_web_researcher)

builder.add_edge(START,"orchestator_web_researcher")
builder.add_conditional_edges("orchestator_web_researcher",route_web_researcher_worker,["worker_web_researcher"])
builder.add_edge("worker_web_researcher","aggregater_web_researcher")
builder.add_edge("aggregater_web_researcher",END)

web_researcher_agent = builder.compile(checkpointer=InMemorySaver())