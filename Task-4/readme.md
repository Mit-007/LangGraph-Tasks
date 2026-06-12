# Call Quality Analysis Agent

## Overview

**Call Quality Analysis Agent** is a LangGraph-based workflow application that analyzes customer call transcripts through a multi-step AI pipeline.

The system automatically:

* Extracts issues from call transcripts
* Classifies issue severity
* Generates remediation recommendations
* Produces a structured quality report
* Supports human-in-the-loop review for uncertain extractions and report approval

The application is exposed through **FastAPI** endpoints and can be tested directly using **Swagger UI**.

---

## Architecture

### Technology Stack

* **LangGraph** – Workflow orchestration
* **FastAPI** – REST API layer
* **LLM** – Issue extraction, classification, and report generation
* **Server-Sent Events (SSE)** – Real-time streaming responses
* **Human-in-the-Loop Interrupts** – Approval and review checkpoints

---

## API Endpoints

### Swagger UI

After starting the application, open:

```text
http://localhost:8000/docs
```

---
## How to run 

Task-4 is a REST API application built with FastAPI.

Navigate to the task folder:

```bash
cd Task-4
```

Start the API server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

### API Diagram

<img width="1692" height="335" alt="Api_endpoint" src="https://github.com/user-attachments/assets/ee882325-b80b-4d9c-ab43-bfa8a1ac851c" />

---

## 1. POST `/analyze`

Analyze a transcript and execute the complete workflow.

### Request

```json
{
  "transcript": "Customer is unable to login after password reset..."
}
```

### Response

Returns:

* Final agent state
* Thread ID for future operations

### Example Response

```json
{
  "thread_id": "abc123",
  "result": {}
}
```

---

## 2. POST `/stream`

Works exactly like `/analyze`, but streams the output of each node as it executes.

### Features

* Real-time execution updates
* Server-Sent Events (SSE)
* Useful for monitoring workflow progress

### Request

```json
{
  "transcript": "Customer is unable to login after password reset..."
}
```

### Response

```text
event: node_update
data: {...}

event: node_update
data: {...}

event: completed
data: {...}
```

---

## 3. POST `/resume`

Used to resume a workflow that was paused at a human review checkpoint.

The endpoint requires a valid `thread_id` from a previous run.

---

### Scenario 1: Issue Review Approval

When the workflow pauses at **Issue Review**, the user can:

#### Approve All Issues

```json
{
  "thread_id": "your_thread_id",
  "approval": true
}
```

#### Remove Specific Issues

```json
{
  "thread_id": "your_thread_id",
  "approval": false,
  "remove_issues": [
    "001",
    "002",
    "004"
  ]
}
```

The specified issue IDs will be removed before continuing the workflow.

---

### Scenario 2: Draft Report Approval

When the workflow pauses at **Draft Review**, the user can:

#### Approve Draft

```json
{
  "thread_id": "your_thread_id",
  "approval": true
}
```

---

#### Request Draft Changes

```json
{
  "thread_id": "your_thread_id",
  "approval": false,
  "fixes": [
    {
      "issue": "issue1",
      "solution": "solution1"
    },
    {
      "issue": "issue2",
      "solution": "solution2"
    }
  ]
}
```

The provided fixes replace the existing recommendations and the workflow continues from the draft review stage.

---

## 4. GET `/status/{thread_id}`

Retrieve the current execution status of a workflow.

### Example

```http
GET /status/abc123
```

### Response

```json
{
  "thread_id": "abc123",
  "result": "last state value"
}
```
---

# Workflow Design

<img width="338" height="829" alt="agent_workflow" src="https://github.com/user-attachments/assets/d7823315-a7e7-4f19-9d55-88c4e518e416" />

---

## Workflow Pipeline

### 1. `ingest_transcript`

#### Purpose

Validates the incoming transcript before processing.

#### Responsibilities

* Receives workflow input
* Validates transcript content
* Ensures transcript is not empty

#### Validation

If the transcript is empty:

```python
ValueError("Transcript cannot be empty")
```

---

### 2. `extract_issues`

#### Purpose

Extract actionable issues from the call transcript.

#### Output Schema

```json
{
  "id": "001",
  "issue": "Platform login authentication failure",
  "description": "Users are currently unable to log in to the platform.",
  "confidence_score": 1.0
}
```

#### Fields

| Field            | Description                              |
| ---------------- | ---------------------------------------- |
| id               | Unique issue identifier                  |
| issue            | Short issue title                        |
| description      | Detailed explanation of the issue        |
| confidence_score | Model confidence that the issue is valid |

---

### Confidence-Based Human Review

If any extracted issue has:

```text
confidence_score < 0.70
```

the workflow routes to:

```text
human_review_for_extract_issues
```

This allows a human reviewer to verify uncertain issues before continuing.

---

### 3. `human_review_for_extract_issues`

#### Purpose

Review issues that have low confidence scores.

#### Responsibilities

* Display uncertain issues
* Accept reviewer feedback
* Remove incorrect issues if necessary

#### User Action

The reviewer submits issue IDs to remove through the `/resume` endpoint.

---

### 4. `classify_severity`

#### Purpose

Determine the business impact of each issue.

#### Severity Levels

| Severity | Description                                 |
| -------- | ------------------------------------------- |
| Low      | Minor impact                                |
| Medium   | Moderate impact                             |
| High     | Significant impact                          |
| Critical | Severe impact requiring immediate attention |

#### Output Example

```json
{
  "issue_id": "001",
  "severity": "High"
}
```

---

### 5. `generate_fix`

#### Purpose

Generate remediation recommendations for every issue.

#### Responsibilities

* Produce actionable fixes
* Generate implementation steps
* Create recommendations for issue resolution
* Calculate an overall solution score

#### Example Output

```json
{
  "issue": "issue_name",
  "fix": [
    "Verify authentication service",
    "Reset failed login cache",
    "Validate user credentials"
  ]
}
```

---

### 6. `draft_report`

#### Purpose

Create the final structured report.

#### Generated Report Format

```json
{
  "issues": [],
  "severity_summary": {},
  "recommended_fixes": [],
  "overall_score": 0.0
}
```

#### Included Sections

* Extracted issues
* Severity distribution
* Recommended fixes
* Overall quality score

---

### Draft Approval Logic

After generating the report:

#### Auto Approval Path

If **all issues are classified as Low severity**, the workflow proceeds directly to completion.

```text
draft_report
    ↓
complete
```

---

#### Human Review Path

If **any issue is Medium, High, or Critical**, the workflow pauses for review.

```text
draft_report
    ↓
human_review_for_draft
```

---

### 7. `human_review_for_draft`

#### Purpose

Allow human validation of the generated report and remediation recommendations.

#### Reviewer Options

##### Approve

```json
{
  "thread_id": "your_thread_id",
  "approval": true
}
```

Workflow proceeds to completion.

---

##### Request Changes

```json
{
  "thread_id": "your_thread_id",
  "approval": false,
  "fixes": [
    {
      "issue": "issue1",
      "solution": "updated solution"
    }
  ]
}
```

Workflow updates the recommendations and regenerates the final report.

---

# Workflow Routing Summary

```text
ingest_transcript
        │
        ▼
extract_issues
        │
        ├── confidence_score < 0.70
        │
        ▼
human_review_for_extract_issues
        │
        ▼
classify_severity
        │
        ▼
generate_fix
        │
        ▼
draft_report
        │
        ├── All Low Severity
        │         │
        │         ▼
        │      Complete
        │
        └── Any Medium/High/Critical
                  │
                  ▼
        human_review_for_draft
                  │
                  ▼
               Complete
```

---

# Human-in-the-Loop Design

The workflow contains two approval checkpoints:

## Issue Validation Review

Triggered when:

```text
confidence_score < 0.70
```

Purpose:

* Validate uncertain issue extraction
* Remove false positives

---

## Draft Report Review

Triggered when:

```text
Severity != Low
```

Purpose:

* Review generated recommendations
* Modify remediation plans
* Approve final report before completion

---

