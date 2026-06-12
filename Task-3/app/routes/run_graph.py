from fastapi import APIRouter
from app.agent import researcher_agent
import uuid

router = APIRouter(prefix="", tags=["Researcher-Agent"])

@router.post("/runGraph")
def rerunGraph(Question : str):
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    input_state = {
        'user_input' : Question,
        'researchers_list' : [],
        'researchers_output' : [],
        'final_report' : "******"
    }
    result = researcher_agent.invoke(input_state,config)
    return{
        # "user_input" : "result"["user_input"],
        # "final_report":result["final_report"]    
        "user_input" : Question,
        "final_report":result["final_report"],
        "thread_id" : thread_id       
    }