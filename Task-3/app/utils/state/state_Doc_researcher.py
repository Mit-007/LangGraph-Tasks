from typing import TypedDict , Annotated 
from pydantic import BaseModel
import operator

#  -> llm output schema
class Doc_researcher_llm_sceama(BaseModel):
    topic : str
    sub_querys : list[str]

class Doc_researcher_aggregator_sceama(BaseModel):
    final_report : str


# -> worker State
class Doc_researcher_worker_State(TypedDict):
    sub_query : str
    result : str


#  -> Main Graph state
class Doc_researcher_State(TypedDict):
    topic : str
    sub_querys : list[str]
    workers_output : Annotated[list[Doc_researcher_worker_State],operator.add]
    final_result : str
