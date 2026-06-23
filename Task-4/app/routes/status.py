from fastapi import APIRouter ,HTTPException
from app.agent import agent
from app.services.logger import logger

router = APIRouter(prefix="" , tags=["Call Quality Analysis Agent"])

@router.get("/status/{thread_id}")
def getStatus(thread_id : str):
    """Retrieve the current execution state of the graph for the given thread ID."""
    try:
        if thread_id.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="Thread ID cannot be empty."
            )
    
        config = {"configurable": {"thread_id":thread_id}}
        current_state = agent.get_state(config)

        if current_state.interrupts != ():
            return {
                "message": "Graph Is Paused For Human Approval !!", 
                "Interrupt" : current_state.interrupts,
                "Next_Node" :current_state.next,
                "Values" : current_state.values
            }


        return{
            "message" : "graph Is Completed",
            "Final_Draft" : current_state.values['draft_report']
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to resume graph.{e}"
        )