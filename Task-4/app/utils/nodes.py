from app.utils.states import *
from typing import Literal
from langgraph.types import interrupt
from app.services.prompt_services import *
from app.services.llm_services import llm
from app.services.logger import logger


# =============
# ingest_transcript
# =============
def ingest_transcript(state : Agent_schema) ->Agent_schema: 
    logger.info("Node:-ingest_transcript")
    try:
        transcript = state.call_transcript

        if not transcript or not transcript.strip():
            raise ValueError("Transcript is empty")
        
        return {
            "call_transcript": transcript
        }

    except Exception as e:
        logger.error(f"❌ Exception: {e}")

        return {
            "transcript": ""
        }

# =============
# extract_issues
# ============= 
def extract_issues(state : Agent_schema) ->Agent_schema:
    logger.info("Node:-extract_issues")
    try:
        transcript = state.call_transcript

        if transcript.strip() == "":
            raise ValueError("Transcript is empty, That Why Not Generate Issues")

        logger.debug("👨 Human : Generate Issues")

        if not llm:
            raise ValueError("LLM service is not available.")

        issue_extraction_prompt = ISSUE_EXTRACTION_PROMPT.format(transcript = state.call_transcript)
        structured_llm = llm.with_structured_output(issues_extract_schema)
        result = structured_llm.invoke(issue_extraction_prompt)

        logger.debug(f"🤖 AI : {result}")

        return{
            'issues': result.issues
        }

    except Exception as e:
        logger.error(f"❌ Exception: {e}")
        return {
            'issues' : []
        }


# =============
# route_human_review_for_extract_issues
# =============
def route_human_review_for_extract_issues(state: Agent_schema) -> Literal["human_review_for_extract_issues", "classify_severity"]:
    logger.info("Node:-route_human_review_for_extract_issues")
    try : 

        issues = state.issues

        if issues == [] :
            raise ValueError("Issues List is empty")
        
        for issue in state.issues:
            if issue["confidence_score"] < 0.7 :
                return "human_review_for_extract_issues"

        return "classify_severity"
    
    except Exception as e:
        logger.error(f"❌ Exception: {e}")

        return "classify_severity"

# =============
# extract_issues
# =============
def human_review_for_extract_issues(state : Agent_schema) -> Agent_schema :
    logger.info("Node:-human_review_for_extract_issues")
    list_low_score_issues = []
    for issue in state.issues:
        if issue["confidence_score"] < 0.7 :
            list_low_score_issues.append(issue)


    interrupt_mess = f"""\nI Fetch Some issues , with confusion please clasify the given list of issues , are real or not !!\nif you remove perticular issues then , return isseus Id like : ["001","002","003"] ,\nif not a sngle removal than give empty list : []\n\nlist of issues :\n{list_low_score_issues}\n"""


    logger.critical(f"🛑 Interrupt :Human approval for Low Qulity 'Issues'")
    logger.debug(f"Interrupt  : {interrupt_mess}")

    human_issues_replay= interrupt(interrupt_mess)

    logger.debug(f"Human Approval : {human_issues_replay['approval']}")

    try:
        if human_issues_replay['approval'] == False : 
            if "remove_issues" not in human_issues_replay:
                raise ValueError("No issue ID provided for remove")
            logger.info(f"Issues Rejected By Human : {human_issues_replay['remove_issues']}")
            ids_to_remove  = human_issues_replay['remove_issues']
            new_issues = [
                issue
                for issue in state.issues
                if issue["id"] not in ids_to_remove
            ]
        else :
            new_issues = state.issues

        return {
            "issues" : new_issues
        }
    except Exception as e:
        logger.error(f"❌ Exception: {e}")
        return {
            'issues' : state.issues
        }

# =============
# classify_severity
# =============
def classify_severity(state : Agent_schema) ->Agent_schema:
    logger.info("Node:-classify_severity")
    try :
        issues = state.issues

        if issues == [] :
            raise ValueError("Issues List is empty")
        
        logger.debug("👨 Human : Generate Severity")

        if not llm:
            raise ValueError("LLM service is not available.")

        severity_classify_prompt = SEVERITY_CLASSIFY_PROMPT.format(issues = state.issues)
        structured_llm = llm.with_structured_output(severity_classify_schema)
        result = structured_llm.invoke(severity_classify_prompt)

        logger.debug(f"🤖 AI : {result}")

        return { 
            'severity' : result.severity
        }
    
    except Exception as e:
        logger.error(f"❌ Exception: {e}")
        return {
            'severity' : []
        }

# =============
# generate_fix
# =============
def generate_fix(state : Agent_schema) ->Agent_schema:
    logger.info("Node:-generate_fix")
    try:

        severity = state.severity

        if severity == [] :
            raise ValueError("severity List is empty")
        
        logger.debug("👨 Human : Generate fixes")

        if not llm:
            raise ValueError("LLM service is not available.")

        generate_fixes_prompt= GENERATE_FIXES_PROMPT.format(issues_with_severity = state.severity)
        structured_llm = llm.with_structured_output(generate_fixes_schema)
        result = structured_llm.invoke(generate_fixes_prompt)

        logger.debug(f"🤖 AI : {result}")

        return {
            'fixes' : result.solutions,
            'overall_score' : result.overall_score
        }
    
    except Exception as e:
        logger.error(f"❌ Exception: {e}")
        return {
            'fixes' : [],
            'overall_score' : 0.0
        }


# =============
# draft_report
# =============
def draft_report(state : Agent_schema) ->Agent_schema:
    logger.info("Node:-draft_report")

    try : 

        fixes = state.fixes

        if fixes == [] :
            raise ValueError("Solution List is empty")
        
        draft = {
            'issues' : state.issues,
            'severity_summary' : state.severity,
            'recommended_fixes' : state.fixes,
            'overall_score': state.overall_score
        }

        return {
            'draft_report' : draft
        }

    except Exception as e:
        logger.error(f"❌ Exception: {e}")
        return {
            'draft_report' : {}
        }


# =============
# human_review_for_draft
# =============
def human_review_for_draft(state : Agent_schema) ->Agent_schema:
    logger.info("Node:-human_review")

    interrupt_mess = f"""\n i make final report draft :\n{state.draft_report}\n\nIf you wnat to change in draft report give changes Dict Of Solution ,or not want change that section give 'None' """

    logger.critical(f"🛑 Interrupt :Human approval for 'Draft' ")
    logger.debug(f"Interrupt  : {interrupt_mess}")

    human_draft_replay= interrupt(interrupt_mess)

    logger.debug(f"Human Approval : {human_draft_replay['approval']}")

    try :

        if human_draft_replay['approval']== False :
            if "fixes" not in human_draft_replay:
                raise ValueError("No fixes provided")
            logger.debug(f"New Solution Given BY Human : \n {human_draft_replay['fixes']}")
            state.draft_report['recommended_fixes'] = human_draft_replay['fixes']
        
        return {
            'draft_report':state.draft_report
    }

    except Exception as e:
        logger.error(f"❌ Exception: {e}")
        return {
            'draft_report' : state.draft_report
        }


# =============
# route_human_review_for_draft
# =============
def route_human_review_for_draft(state: Agent_schema) -> Literal["human_review", "END"]:
    logger.info("Node:-route_human_review")

    try:

        draft_report = state.draft_report

        if draft_report == {} :
            raise ValueError("Draft IS Not Genearated")
    
        for sol in state.fixes:
            if sol["severity"].lower() != "low":
                return "human_review_for_draft"

        return "END"

    except Exception as e:
        logger.error(f"❌ Exception: {e}")
        return "END"


