from fastapi import APIRouter ,HTTPException
from pydantic import BaseModel
from app.agent  import researcher_agent
from app.services.logger import logger

router = APIRouter(prefix="", tags=["Researcher-Agent"])

class TimeTravelSchema(BaseModel):
    new_Question : str
    thread_id : str 

@router.post("/timeTravel")
def timeTravel(data : TimeTravelSchema):
    """
    Perform time travel by updating the user input at a previous execution state.

    The function locates the checkpoint immediately before the orchestrator
    node, forks the graph execution with the new user input, resumes execution
    from that point, and returns the updated final report.
    """
    
    try:
        if not data.new_Question.strip() or not data.thread_id.strip(): 
            raise HTTPException( status_code=400, detail="Question/Thread_id cannot be empty.")

        config = {"configurable": {"thread_id": data.thread_id}}
        state_list = researcher_agent.get_state_history(config)
        
        for state in state_list:
            if len(state.next)==1 and state.next[0] == 'orchestator':
                new_config = state.config

        fork_state =researcher_agent.update_state(new_config,values={"user_input": data.new_Question})

        result = researcher_agent.invoke(None ,config)

        return {
            "user_input" : result["user_input"],
            "final_report":result["final_report"]    
        }
    
    except HTTPException:
        raise

    except Exception as e: 
        logger.error(e) 
        raise HTTPException( status_code=500, detail=f"Time travel execution failed. {e}" )