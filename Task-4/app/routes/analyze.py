from fastapi import APIRouter
from app.agent import agent
import uuid

router = APIRouter(prefix="", tags=["Call Quality Analysis Agent"])

@router.post("/analyze")
def runGraph(transcript : str):
    """Create a new graph execution and process the provided transcript."""
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    input_state = {
        "call_transcript": transcript,
        "issues": [],
        "severity": [],
        "fixes": [],
        "draft_report": {
            "issues": [],
            "severity_summary": [],
            "recommended_fixes": [],
            "overall_score": 0.0
        },
        "overall_score": 0.0
    }
    result = agent.invoke(input_state,config)

    if result["__interrupt__"] :
        return {
            "thread_id" : thread_id ,
            "AI : " : result["__interrupt__"][0].value
        } 
    
    return{
        "result" : result ,
        "thread_id" : thread_id       
    }