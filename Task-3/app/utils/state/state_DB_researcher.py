from typing import TypedDict , Annotated ,Any
from pydantic import BaseModel
import operator


class Db_query_schema(BaseModel):
    query_name  : str
    query : str

class DB_researcher_llm_schema(BaseModel):
    sub_querys : list[Db_query_schema]

class DB_researcher_aggregator_schema(BaseModel):
    final_answer : str



class DB_researcher_worker_State(TypedDict):
    sub_query : Db_query_schema
    result : str
    db_path : str

class DB_researcher_State(TypedDict):
    query : str
    db_path : str
    sub_querys : list[Db_query_schema]
    schema_of_collection : dict
    workers_output : Annotated[list[DB_researcher_worker_State],operator.add]
    final_result : str
