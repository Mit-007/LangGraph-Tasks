from fastapi import APIRouter
from pydantic import BaseModel
from app.agent  import researcher_agent

router = APIRouter(prefix="", tags=["Researcher-Agent"])

class TimeTravelSchema(BaseModel):
    new_Question : str
    thread_id : str 

@router.post("/timeTravel")
def timeTravel(data : TimeTravelSchema):
    config = {"configurable": {"thread_id": data.thread_id}}
    state_list = researcher_agent.get_state_history(config)
    if data.step_No>= len("state_list"):
        return{
            "message" : "Current Step Not Present in Graph(Heigher Value)"
        }
    
    for state in state_list:
        if len(state.next)==1 and state.next[0] == 'orchestator':
            new_config = state.config

    # print(state_list)

    fork_state =researcher_agent.update_state(new_config,values={"user_input": data.new_Question})

    result = researcher_agent.invoke(None ,config)

    return {
        "user_input" : result["user_input"],
        "final_report":result["final_report"]    
    }