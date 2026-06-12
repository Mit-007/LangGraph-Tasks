from typing import TypedDict, Annotated ,Literal
import operator
from pydantic import BaseModel


class taskSchema(TypedDict):
    researcher_name : Literal['DB_researcher_agent','Doc_researcher_agent','web_researcher_agent']
    query : str

class orchestator_llm_schema(BaseModel):
    researchers_list : list[taskSchema]

class aggregator_llm_schema(BaseModel):
    final_answer : str

class WorkerState(TypedDict):
    researcher_name : str
    query : str
    result : dict 

class MainState(TypedDict):
    user_input : str
    researchers_list : list[taskSchema]
    researchers_output : Annotated[list[str],operator.add]
    final_report : str
