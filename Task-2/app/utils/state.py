from typing import TypedDict, Literal ,Optional
from typing import Literal, Optional, Union
from pydantic import BaseModel

# =========
# tools Args
# =========
class CalArgs(BaseModel):
    first_nums: float
    second_nums: float
    operation: Literal["add", "sub", "mul", "div"]

class WebArgs(BaseModel):
    query: str
    max_result: int

class PythonReplArgs(BaseModel):
    code: str


# =========
# LLm Schema
# =========
class LLMResponse(BaseModel):
    final_answer: str
    tool_call: bool
    through: str

    tool_name: Optional[
        Literal["calculator", "web_search", "python_repl"]
    ] = None

    tool_args: Optional[
        Union[
            CalArgs,
            WebArgs,
            PythonReplArgs
        ]
    ] = None


# =========
# Agent state Schema
# =========
class AgentState(TypedDict):
    question : str
    final_answer : str
    iteration_count : int
    user_approval : str
    tool_call : bool
    through : str
    tool_name: Optional[Literal["calculator", "web_search", "python_repl"]] = None
    tool_args: Optional[dict] = None
    tool_call_log : list[dict]
    tool_result : dict