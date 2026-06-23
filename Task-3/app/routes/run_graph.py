from fastapi import APIRouter ,HTTPException
from app.agent import researcher_agent
from app.services.logger import logger
import uuid

router = APIRouter(prefix="", tags=["Researcher-Agent"])

@router.post("/runGraph")
def rerunGraph(Question : str):
        
    try:
        if not Question or not Question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty."
            )


        """Run a new research workflow for the provided question."""
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        input_state = {
            'user_input' : Question,
            'researchers_list' : [],
            'researchers_output' : [],
            'final_report' : ""
        }
        result = researcher_agent.invoke(input_state,config)
        return{
            "user_input" : Question,
            "final_report":result["final_report"],
            "thread_id" : thread_id       
        }
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to execute research graph. {e}"
        )