from fastapi import APIRouter ,HTTPException
from app.agent import researcher_agent
from app.services.logger import logger

router = APIRouter(prefix="", tags=["Researcher-Agent"])

@router.post("/rerunGraph/{thread_id}")
def rerunGraph(thread_id : str):
    """Resume graph execution from the last checkpoint using the provided thread ID."""
    
    try:
        if thread_id.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="Thread ID cannot be empty."
            )

        config = {"configurable": {"thread_id": thread_id}}
        result = researcher_agent.invoke(None,config)

        return{
            "user_input" : result["user_input"],
            "final_report":result["final_report"]       
        }
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to resume graph.{e}"
        )