from typing import TypedDict , Annotated 
from pydantic import BaseModel
import operator

#  -> llm output schema
class web_researcher_llm_sceama(BaseModel):
    topic : str
    sub_topic : list[str]

class web_researcher_aggregator_sceama(BaseModel):
    final_answer : str


# -> worker State
class web_researcher_worker_State(TypedDict):
    sub_topic : str
    result : str


#  -> Main Graph state
class web_researcher_State(TypedDict):
    topic : str
    sub_topics : list[str]
    workers_output : Annotated[list[web_researcher_worker_State],operator.add]
    final_result : str
