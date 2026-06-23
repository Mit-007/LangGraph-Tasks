# 🚀 Task-3: Parallel Subgraphs + Checkpointing

A scalable **multi-agent research pipeline** built with **LangGraph** that dynamically distributes work across multiple specialized agents, executes them **in parallel**, aggregates their outputs into a unified response, and supports **checkpointing, persistence, graph resumption, and time travel execution**.

The system is designed to demonstrate advanced LangGraph concepts such as **dynamic fan-out using `Send()`**, **parallel subgraphs**, **state isolation**, **checkpoint recovery**, and **thread-based execution persistence**.

---

# 📖 Project Overview

This project implements a **parent orchestrator graph** that intelligently analyzes a user query and delegates research tasks to multiple specialized agents.

The architecture consists of:

- 🎯 **One Parent Research Agent**
- 🌐 **Web Research Agent**
- 🗄️ **Database Research Agent**
- 📄 **Document Research Agent**


The parent graph dynamically decides which research agents should be executed and launches them **concurrently** using LangGraph's **`Send()` API**.

Each research agent works independently with its **own isolated state**, processes the assigned task through multiple internal nodes, and produces its own result.

After all parallel executions finish, an **Parent Agent** combines the outputs into a single comprehensive response.

---

# 🏗️ Multi-Agent Architecture

The entire system follows an **Orchestrator Pattern**, where a central controller manages multiple specialized worker agents.

Each sub-agent is capable of running **independently**, but together they form a collaborative research pipeline capable of solving more complex tasks.

```
                    User Question
                           │
                           ▼
                  ┌─────────────────┐
                  │  Orchestrator   │
                  └─────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
  Web Researcher    DB Researcher    Doc Researcher
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Aggregator  │
                    └─────────────┘
                           │
                           ▼
                    Final Synthesized Answer
```

---


# 🔄 LangGraph Workflow

The graph follows the execution flow shown below.

<img width="126" height="432" alt="Task-3_workflow" src="https://github.com/user-attachments/assets/22227b15-c5b9-402c-a967-75313d1e60b1" />

---

# ⚙️ How Parallel Execution Works

Unlike sequential pipelines, this project executes multiple research agents **simultaneously**.

The orchestrator first analyzes the user's query and determines which agents are required.

Using LangGraph's **dynamic `Send()` API**, it dispatches tasks to multiple subgraphs at runtime.

Each subgraph:

- receives its own isolated state
- executes independently
- performs its internal processing
- generates its own research output

Since all agents execute concurrently, the total execution time is significantly reduced compared to sequential processing.

Timestamp logs generated during execution demonstrate that all three agents start processing at nearly the same time, proving true parallel execution.

```
2026-06-12 15:46:52 | INFO | 🧠 Start Researcher : DB_researcher_agent
2026-06-12 15:46:54 | INFO | 🧠 End Researcher : DB_researcher_agent
```

Once every subgraph completes, the Aggregator waits for all outputs and merges them into one high-quality synthesized answer.

---

# 🧠 Graph Nodes Explanation

## 1️⃣ Orchestrator Node

The Orchestrator acts as the central decision-making component of the graph.

Its responsibilities include:

- Receiving the user's question
- Understanding the research objective using an LLM
- Identifying which research agents are relevant
- Dynamically spawning parallel subgraphs
- Dispatching work using LangGraph's `Send()` API

Instead of relying on predefined static edges, the orchestrator dynamically creates worker tasks at runtime based on the user's request.

This makes the system flexible and easily extensible.

---

## 2️⃣ Worker Nodes (Parallel Subgraphs)

The Worker stage consists of three independent research agents.

Each agent has:

- its own isolated state
- multiple internal nodes
- independent execution path
- dedicated responsibility

---

Because all three workers execute simultaneously, they significantly reduce total response latency while maintaining independent state management.

---

## 3️⃣ Aggregator Node

The Aggregator executes only after all worker agents complete.

Its responsibilities include:

- collecting outputs from all workers
- removing redundant information
- combining complementary findings
- generating a coherent final response
- producing a single synthesized research answer

The Aggregator transforms multiple independent research outputs into one well-structured answer for the user.

---

# 💾 Persistence & Checkpointing

This project integrates LangGraph checkpointing to provide durable execution.

Features include:

- SQLite-based checkpoint storage
- Thread-specific graph persistence
- Resume execution after interruption
- Recovery from simulated crashes
- State restoration
- Historical execution tracking

Every graph execution is associated with a unique **thread ID**, allowing the graph to continue execution from the last saved checkpoint.

---

# 🔄 Resume Execution

If execution is interrupted (for example, by a simulated `KeyboardInterrupt`), the graph state is automatically saved.

Using the stored **thread ID**, the graph can later resume from the exact checkpoint without restarting from the beginning.

This avoids repeating already completed computations.

---

# ⏪ Time Travel Execution

The project also supports **Time Travel**.

Instead of restarting the graph from scratch, execution can jump back to a previous checkpoint step.

From that step:

- state can be modified
- input can be changed
- execution continues from the selected checkpoint

This feature is extremely useful for debugging, experimentation, and workflow replay.

---

# 🛠️ Tech Stack

| Technology | Purpose |
|------------|----------|
| Python | Programming Language |
| LangGraph | Multi-Agent Workflow Framework |
| LangChain | LLM Integration |
| FastAPI | REST API Development |
| SQLite | Graph Checkpoint Persistence |
| SqliteSaver | LangGraph Checkpointer |
| Uvicorn | ASGI Server |
| OpenAI / LLM | Decision Making & Synthesis |

---

# ▶️ Running the Project

## Step 1

Open a terminal.

```bash
cd Task-3
```

---

## Method 1 — Run Using Python

```bash
python -m app.main
```

This executes the graph directly from the Python entry point.

---

## Method 2 — Run Using FastAPI

Start the FastAPI server:

```bash
uvicorn app.mainApi:app --reload
```

After the server starts, open:

```
http://127.0.0.1:8000/docs
```

to access the interactive Swagger UI.

---

# 🌐 API Endpoints

The project exposes three REST APIs.

---

## 1️⃣ `/runGraph`

Runs a completely new graph execution.

### Input

```json
{
    "question": "Your research question"
}
```

### Functionality

- Creates a new graph execution
- Starts the orchestrator
- Launches parallel research agents
- Aggregates results
- Returns the complete graph state

### Response

Returns the final execution state including synthesized research output.

---

## 2️⃣ `/rerunGraph/{thread_id}`

Resumes a previously interrupted graph execution.

### Input

- `thread_id`

### Functionality

- Loads saved checkpoint
- Restores graph state
- Continues execution from the last checkpoint
- Returns the completed execution state

This endpoint demonstrates LangGraph persistence and checkpoint recovery.

---

## 3️⃣ `/timeTravel`

Re-executes the graph from second step (orchestator node). with new values.

### Input

```json
{
    "thread_id": "...",
    "new_question": "Modified question"
}
```

### Functionality

- Loads historical checkpoint
- Restores graph state from selected step
- Replaces the input with a new question
- Re-executes the remaining workflow
- Returns the updated execution state

This endpoint demonstrates LangGraph's time travel capability.
---
### ⚙️ `constants.py`

The `constants.py` file centralizes all configurable values used throughout the project. Keeping these values in one place makes the application easier to maintain and allows important parameters to be updated without modifying the core logic.

| Constant                 | Description                                                                                             |
| ------------------------ | ------------------------------------------------------------------------------------------------------- |
| `OUTPUT_DIMENSIONALITY`  | Embedding vector dimension used for query generation.                                                   |
| `MAX_RESULTS_WEB_SEARCH` | Maximum number of results retrieved from the Tavily web search for each query.                          |
| `TOP_K`                  | Number of top relevant documents retrieved from the RAG vector store.                                   |
| `MAX_SUB_QUERY_FOR_DOC`  | Maximum number of sub-queries generated by the document researcher agent.                               |
| `TEMPERATURE`            | Controls the randomness of LLM responses. A value of `0` produces deterministic and consistent outputs. |


---

# 🤖 Run Individual Sub-Agents

In addition to the complete multi-agent workflow, each research agent is implemented as an independent and fully runnable project.

If you want to understand the internal architecture or test each agent separately, you can run them individually by following their dedicated documentation.

### Available Agent Documentation

* 📄 **DB_README.md** — Database Research Agent
* 📄 **DOC_README.md** — Document Research Agent
* 📄 **WEB_README.md** — Web Research Agent


Running the agents individually is recommended for gaining a deeper understanding of how each specialized component works before exploring the complete parallel multi-agent orchestration pipeline.
