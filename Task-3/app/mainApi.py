from fastapi import FastAPI
from app.routes import time_travel,rerun_graph,run_graph

app = FastAPI()

app.include_router(run_graph.router)
app.include_router(rerun_graph.router)
app.include_router(time_travel.router)
