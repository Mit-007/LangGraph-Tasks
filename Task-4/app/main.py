from fastapi import FastAPI
from app.routes import analyze,resume,status,stream

app = FastAPI()

app.include_router(stream.router)
app.include_router(analyze.router)
app.include_router(status.router)
app.include_router(resume.router)


