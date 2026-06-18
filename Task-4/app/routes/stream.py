from fastapi import APIRouter
from app.agent import agent
import uuid
from fastapi.sse import EventSourceResponse
from collections.abc import AsyncIterable 
from app.utils.states import Agent_schema

router = APIRouter(prefix="", tags=["Call Quality Analysis Agent"])

@router.post("/stream", response_class=EventSourceResponse)
async def runGraph(transcript : str) -> AsyncIterable[Agent_schema]:
    """
    Create a new graph execution and stream its execution events.
    """
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    input_state = {
        "call_transcript": transcript,
        "issues": [],
        "severity": [],
        "fixes": [],
        "draft_report": {
            "issues": [],
            "severity_summary": [],
            "recommended_fixes": [],
            "overall_score": 0.0
        },
        "overall_score": 0.0
    }
    for event in agent.stream(
        input_state,
        config=config,
        stream_mode="values"
    ):
        yield event

    curr_state = agent.get_state(config)
    if curr_state.interrupts != () : 
        yield {
            f"interrupts : {curr_state.interrupts[0].value}",
        }

    else :
        yield {
            "Current Proceess Are fully Completed !!"
        }

    yield {
        f"thred_id : {thread_id}"
    }