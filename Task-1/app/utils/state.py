from typing import TypedDict , Literal
from pydantic import BaseModel
from langchain_core.messages import AIMessage

class AgentState(TypedDict):
    messages : list[str]
    summary : str
    turn_count : int
    mood : list[Literal["positive","neutral","negative"]]
    answer : str
    summary_status : bool   #if generate then =>True , else => False

class ouput_schema(BaseModel):
    output : AIMessage
    mood : Literal["positive","neutral","negative"]

class summary_schema(BaseModel):
    summary : str
