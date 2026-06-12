from pydantic import BaseModel,Field
from typing import TypedDict

#============ 
# issue_schema
#============

class issue_schema(TypedDict):
    id : str
    issue : str
    description : str
    confidence_score: float = Field(ge=0.0,le=1.0)

class issues_extract_schema(BaseModel):
    issues : list[issue_schema]

    
#============ 
# severity_schema
#============

class severity_schema(TypedDict):
    issue : str
    description : str
    severity : str

class severity_classify_schema(BaseModel):
    severity : list[severity_schema]


#============ 
# fixes_schema
#============

class fixes_schema(TypedDict):
    issue : str
    severity : str
    solution : str

class generate_fixes_schema(BaseModel):
    solutions : list[fixes_schema]
    overall_score : float

#============ 
# draft_schema
#============

class draft_schema(TypedDict):
    issues : list[issue_schema]
    severity_summary : list[severity_schema]
    recommended_fixes : list[fixes_schema]
    overall_score : float

#============ 
# Agent_schema
#============
class Agent_schema(BaseModel):
    call_transcript : str
    issues : list[issue_schema]
    severity : list[severity_schema]
    fixes : list[fixes_schema]
    draft_report : draft_schema
    overall_score : float