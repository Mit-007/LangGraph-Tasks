from app.utils.nodes import *
from app.utils.states import Agent_schema
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph,START,END
from app.core.config import DB_PATH_OF_CHAT_HISTORY
import sqlite3

builder = StateGraph(Agent_schema)

builder.add_node("ingest_transcript",ingest_transcript)
builder.add_node("extract_issues",extract_issues)
builder.add_node("human_review_for_extract_issues",human_review_for_extract_issues)
builder.add_node("classify_severity",classify_severity)
builder.add_node("generate_fix",generate_fix)
builder.add_node("draft_report",draft_report)
builder.add_node("human_review_for_draft",human_review_for_draft)

builder.add_edge(START,"ingest_transcript")
builder.add_edge("ingest_transcript","extract_issues")
builder.add_conditional_edges("extract_issues",route_human_review_for_extract_issues,{'human_review_for_extract_issues' : "human_review_for_extract_issues",'classify_severity':"classify_severity"})
builder.add_edge("human_review_for_extract_issues","classify_severity")
builder.add_edge("classify_severity","generate_fix")
builder.add_edge("generate_fix","draft_report")
builder.add_conditional_edges("draft_report",route_human_review_for_draft,{'human_review_for_draft' : "human_review_for_draft",'END':END})
builder.add_edge("human_review_for_draft",END)

connection = sqlite3.connect(database=DB_PATH_OF_CHAT_HISTORY,check_same_thread=False)

checkpointers = SqliteSaver(conn=connection)

agent = builder.compile(checkpointer=checkpointers)