# Task-2 — Tool-Calling Agent (ReAct Pattern)

## Overview

This project implements a **ReAct-style Tool-Calling Agent** using **LangGraph**.

The agent follows the **Reason → Act → Observe** workflow, where it first analyzes the user's request, decides whether a tool is required, executes the selected tool (with human approval), observes the result, and then either continues reasoning or produces a final answer.

Unlike prebuilt agent frameworks, the complete tool-calling loop is implemented manually, providing full control over:

- Tool selection
- Tool execution
- Human approval workflow
- Iteration control
- Final answer generation

The agent can decide between:

1. **Calling a tool**
2. **Returning a final answer directly**

The workflow continues until a final answer is produced or the maximum iteration limit is reached.

---

## Features

### ✅ Custom ToolNode

A custom ToolNode is implemented that wraps the following tools:

- `web_search`
- `calculator`
- `python_repl`

---

### ✅ Agent Decision Node

The LLM agent node decides whether to:

- Generate a tool call
- Generate a final answer

---

### ✅ Conditional Routing

A `should_continue()` conditional edge determines whether:

- The workflow should continue to a tool call
- The workflow should stop with a final answer

---

### ✅ Max Iteration Guard

To prevent infinite loops:

- Maximum iterations = **10**
- After reaching the limit, the agent returns a graceful fallback response
- It Is changable , place in app/core/constant.py

Example:

```text
Maximum reasoning steps reached.
Unable to complete the request safely.
Please try rephrasing your question.
```

---

### ✅ Streamed Execution

Each reasoning step is streamed and displayed, including:

- Agent reasoning
- Tool call decision
- Tool name
- Tool arguments
- Tool result

---

### ✅ Human-in-the-Loop Approval

Before every tool execution, the workflow pauses and requests user approval.

Example:

```text
Can I use calculator tool? (yes/no)
```

If approved:

```text
yes
```

The tool executes.

If rejected:

```text
no
```

The agent returns without executing the tool.

---

## Project Workflow

The workflow follows a simple ReAct cycle:

```text
Reason
  ↓
Need Tool?
  ↓
Yes → Human Approval → Execute Tool → Observe Result
  ↑                                      ↓
  └──────── Continue Reasoning ──────────┘

No
 ↓
Final Answer
```

---

## How to Run

### Step 1

Recommended: Read the root directory **README.md** first for environment setup instructions.

---

### Step 2

Open a terminal and navigate to the Task-2 directory:

```bash
cd Task-2
```

---

### Step 3

Run the application:

```bash
python -m app.main
```

---

## Graph Structure

### Workflow Diagram

<img width="252" height="273" alt="Task-2_workflow" src="https://github.com/user-attachments/assets/3556e0c9-aa66-4363-8d18-21e6bf9da82d" />


## Nodes Explained

### 1. `call_llm`

**Purpose**

The primary reasoning node.

Responsibilities:

- Analyze the user query
- Decide whether a tool is required
- Select the appropriate tool
- Generate tool arguments
- Produce a final answer when enough information is available

Output:

```python
{
    "tool_call": True/False,
    "tool_name": "...",
    "tool_args": {...},
    "thought": "..."
}
```

---

### 2. `tool_node`

**Purpose**

Executes the selected tool.

Responsibilities:

- Receive tool information from `call_llm`
- Pause execution for user approval
- Execute the requested tool
- Store tool result in state
- Return observation back to the agent

Supported tools:

```text
calculator
web_search
python_repl
```

---

## Conditional Edges

### `should_continue()`

Determines the next step after `call_llm`.

Logic:

```python
if tool_call:
    return "tool_node"
else:
    return END
```

---

### Iteration Guard

Before routing to another tool call:

```python
if iteration_count >= 10:
    return END
```

This prevents infinite loops and ensures graceful termination.

---

## Example Output

### User Query

```text
what is 2+6 ?
```

---

### Agent Execution

```text
============================================== Start =================================================================================

👨 User : what is 2+6 ?

====================
Tool_call_Require : True

tool_name : calculator

Thought :
The user is asking for a simple arithmetic calculation involving two numbers,
which is best handled by the calculator tool.

tool_args :
{
    'first_nums': 2.0,
    'second_nums': 6.0,
    'operation': 'add'
}
----------

🛑 Interrupt :
Can I use the calculator tool? (yes/no)

enter the approval : yes

----------

🔧 Tool Result :
{
    'Answer': 8.0
}

====================

====================
Tool_call_Require : False

tool_name : None

Thought :
The calculation has already been performed and the result is available
in the tool history.

tool_args : None
----------

----------------
| ✅ Final Output |
----------------

Question :
what is 2+6 ?

Final Answer :
The result of 2 + 6 is 8.

----------------------------
| Tool Call Summary |
----------------------------

[1]

Tool Name :
calculator

Tool Arguments :
{
    'first_nums': 2.0,
    'second_nums': 6.0,
    'operation': 'add'
}

Tool Result :
{
    'Answer': 8.0
}

============================================== End =================================================================================
```

---

## Key Learning Concepts

This project demonstrates:

- LangGraph fundamentals
- ReAct Agent pattern
- Manual tool-calling implementation
- Conditional graph routing
- Human-in-the-loop workflows
- Interrupt and resume patterns
- State management
- Iteration control
- Tool execution pipelines
- Streaming agent responses

---

## Tech Stack

- Python
- LangGraph
- LangChain
- OpenAI / LLM Provider
- Pydantic

---