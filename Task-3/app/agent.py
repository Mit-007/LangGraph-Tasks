from app.utils.nodes.nodes_main_graph import *
from app.utils.state.states import MainState
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.sqlite import SqliteSaver
from app.core.config import DB_PATH_OF_CHAT_HISTORY
import sqlite3

builder = StateGraph(MainState)

builder.add_node("orchestator",orchestator)
builder.add_node("worker",worker)
builder.add_node("aggregater",aggregater)

builder.add_edge(START,"orchestator")
builder.add_conditional_edges("orchestator",route_workers,["worker"])
builder.add_edge("worker","aggregater")
builder.add_edge("aggregater",END)

connection = sqlite3.connect(database=DB_PATH_OF_CHAT_HISTORY,check_same_thread=False)

checkpointers = SqliteSaver(conn=connection)

researcher_agent = builder.compile(checkpointer=checkpointers)