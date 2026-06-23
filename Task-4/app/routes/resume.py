from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from langgraph.types import Command
from app.agent import agent
from app.services.logger import logger
from typing import TypedDict

router = APIRouter(prefix="", tags=["Call Quality Analysis Agent"])

class fixesSchema(TypedDict):
    issue : str
    solution :str

class resumeScheama(BaseModel):
    thread_id : str
    approval : bool 
    remove_issues : list[str] | None = None
    fixes : list[fixesSchema] | None = None


@router.post("/resume")
def rerunGraph(data: resumeScheama):
    """Take Thread Id And human approval Data,Resume the Graph Execution"""
    try:
        if data.thread_id.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="Thread ID cannot be empty."
            )
        config = {"configurable": {"thread_id": data.thread_id}}
        curr_state = agent.get_state(config)
        if curr_state.interrupts == () : 
            result = agent.invoke(None,config)
            
        else :    
            if data.approval==False and (data.fixes==None and data.remove_issues==None) :
                raise HTTPException(status_code=400,detail="Data are Required for Resume Graph!!")
            
            payload = data.model_dump(exclude_none=True)

            result = agent.invoke(
                Command(resume=payload),
                config=config
            )
                
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