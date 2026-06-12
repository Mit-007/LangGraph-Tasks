from fastapi import APIRouter
from app.agent import agent

router = APIRouter(prefix="" , tags=["Call Quality Analysis Agent"])

@router.get("/status/{thread_id}")
def getStatus(thread_id : str):
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