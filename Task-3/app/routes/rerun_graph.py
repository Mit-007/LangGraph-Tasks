from fastapi import APIRouter
from app.agent import researcher_agent

router = APIRouter(prefix="", tags=["Researcher-Agent"])

@router.post("/rerunGraph/{thread_id}")
def rerunGraph(thread_id : str):
    """Resume graph execution from the last checkpoint using the provided thread ID."""
    
    config = {"configurable": {"thread_id": thread_id}}
    result = researcher_agent.invoke(None,config)

    return{
        "user_input" : result["user_input"],
        "final_report":result["final_report"]       
    }