
# from langchain_core.documents import Document
# from pydantic import BaseModel


# class cal_args(TypedDict):
#     first_nums: float
#     second_nums: float
#     operation: Literal["add","sub","mul","div"]

# class web_args(TypedDict):
#     query: str
#     max_result: int

# class pyhton_rep_args(TypedDict):
#     code: str




# class llm_response(BaseModel):
#     final_answer: str
#     tool_call: bool
#     through: str
#     tool_name: Optional[Literal["calculator", "web_search", "python_repl"]] = None
#     tool_args: Optional[Literal[cal_args, web_args ,pyhton_rep_args]] = None

from typing import TypedDict, Literal ,Optional
from typing import Literal, Optional, Union
from pydantic import BaseModel


class CalArgs(BaseModel):
    first_nums: float
    second_nums: float
    operation: Literal["add", "sub", "mul", "div"]


class WebArgs(BaseModel):
    query: str
    max_result: int


class PythonReplArgs(BaseModel):
    code: str


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