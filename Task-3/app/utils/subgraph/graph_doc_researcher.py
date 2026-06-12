from langgraph.graph import StateGraph,START ,END
from app.utils.state.state_Doc_researcher import Doc_researcher_State
from app.utils.nodes.nodes_doc_researcher import *
from langgraph.checkpoint.memory import InMemorySaver

builder = StateGraph(Doc_researcher_State)

builder.add_node("orchestator_Doc_researcher",orchestator_Doc_researcher)
builder.add_node("worker_Doc_researcher",worker_Doc_researcher)
builder.add_node("aggregater_Doc_researcher",aggregater_Doc_researcher)

builder.add_edge(START,"orchestator_Doc_researcher")
builder.add_conditional_edges("orchestator_Doc_researcher",route_Doc_researcher_worker,["worker_Doc_researcher"])
builder.add_edge("worker_Doc_researcher","aggregater_Doc_researcher")
builder.add_edge("aggregater_Doc_researcher",END)

Doc_researcher_agent = builder.compile(checkpointer=InMemorySaver())