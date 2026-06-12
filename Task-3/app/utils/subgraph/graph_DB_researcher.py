from langgraph.graph import StateGraph,START ,END
from app.utils.state.state_DB_researcher import DB_researcher_State
from app.utils.nodes.nodes_DB_researcher import *
from langgraph.checkpoint.memory import InMemorySaver

builder = StateGraph(DB_researcher_State)

builder.add_node("get_schema_list",get_schema_list)
builder.add_node("orchestator_DB_researcher",orchestator_DB_researcher)
builder.add_node("worker_DB_researcher",worker_DB_researcher)
builder.add_node("aggregater_DB_researcher",aggregater_DB_researcher)

builder.add_edge(START,"get_schema_list")
builder.add_edge("get_schema_list","orchestator_DB_researcher")
builder.add_conditional_edges("orchestator_DB_researcher",route_DB_researcher_worker,["worker_DB_researcher"])
builder.add_edge("worker_DB_researcher","aggregater_DB_researcher")
builder.add_edge("aggregater_DB_researcher",END)

DB_researcher_agent = builder.compile(checkpointer=InMemorySaver())