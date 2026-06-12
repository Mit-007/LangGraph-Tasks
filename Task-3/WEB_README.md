
# 🌐 Web Research Agent

A specialized **LangGraph-based research agent** that performs **parallel web searching** by breaking a user's query into multiple sub-queries, searching them simultaneously using the **Tavily Search API**, and synthesizing the results into a single comprehensive answer.

The agent follows an **Orchestrator → Worker → Aggregator** architecture to improve search quality and reduce response latency through parallel execution.

---

# 📖 Project Overview

The Web Research Agent is designed to answer complex research questions by intelligently dividing the original query into smaller independent research tasks.

Instead of performing a single web search, the agent:

* analyzes the user's question,
* generates multiple sub-queries,
* executes all searches in parallel,
* collects the findings,
* and produces one well-structured final response.

This parallel approach enables broader coverage of the topic while reducing total execution time.

---

# ✨ Features

* ✅ Intelligent query decomposition
* ✅ Parallel web searching
* ✅ Tavily Search API integration
* ✅ Multi-node LangGraph workflow
* ✅ Automatic answer synthesis
* ✅ Modular architecture
* ✅ Independent runnable agent

---

# 🏗️ Architecture

<img width="250" height="432" alt="web_researcher" src="https://github.com/user-attachments/assets/438bf9c8-5bff-4ed3-bd6c-eca51cfc4516" />

---

# ⚙️ How the Agent Works

The agent processes a user query through three major stages.

## 1️⃣ Orchestrator Node

The Orchestrator acts as the planner of the workflow.

Its responsibilities include:

* Receiving the user's query
* Understanding the research objective
* Breaking the query into multiple independent sub-queries
* Preparing tasks for parallel execution

Rather than searching the entire question directly, the orchestrator decomposes it into smaller research topics that can be processed simultaneously.

These sub-queries are then forwarded to the Worker node.

---

## 2️⃣ Worker Node

The Worker node is responsible for executing all research tasks.

Each sub-query is processed independently and **in parallel**, allowing multiple web searches to happen at the same time.

The Worker uses the **Tavily Search Tool** to retrieve relevant and up-to-date information from the web.

---

## 3️⃣ Aggregator Node

The Aggregator receives outputs from all parallel workers.

Its responsibilities include:

* Collecting all search results
* Removing duplicate information
* Combining related findings
* Organizing the content logically
* Generating a coherent final answer

The final output is a single synthesized response that incorporates information gathered from multiple web searches.

---

# 🔄 Workflow

```
                User Question
                       │
                       ▼
              ┌─────────────────┐
              │  Orchestrator   │
              └─────────────────┘
                       │
          Generates Multiple Sub Queries
                       │
                       ▼
────────────────────────────────────────────
│          │            │          │
▼          ▼            ▼          ▼
Search    Search      Search     Search
Task 1    Task 2      Task 3     Task N
│          │            │          │
└──────────┴────────────┴──────────┘
                Parallel Execution
                       │
                       ▼
              ┌─────────────────┐
              │   Aggregator    │
              └─────────────────┘
                       │
                       ▼
              Final Synthesized Answer
```

---

# 🛠️ Tech Stack

| Technology          | Purpose                            |
| ------------------- | ---------------------------------- |
| Python              | Programming Language               |
| LangGraph           | Workflow Orchestration             |
| LangChain           | LLM Integration                    |
| Tavily Search API   | Web Search                         |
| Google Gemini / LLM | Query Planning & Answer Generation |

---

# ▶️ Running the Agent

Open a terminal.

```bash
cd Task-3
```

Run the Web Research Agent:

```bash
python -m app.main_web
```

The agent will execute the complete web research workflow and generate a synthesized response.

---

# 🔑 Environment Setup

The Web Research Agent requires a **Tavily API Key** for performing web searches.

Environment configuration:

```env
TAVILY_API_KEY="your_api_key"
```

For complete environment setup instructions, API key generation steps, and `.env` configuration, please refer to the **root `README.md`** of the project.

---

# 📤 Example Output

```
----------------
| 🎯 Topic      |
----------------

What is Retrieval-Augmented Generation (RAG)?

----------------
| 🧩 Sub Topics |
----------------

• What is RAG?
• How does retrieval work?
• What are vector databases?
• What are embeddings?
• Advantages of RAG
• Applications of RAG

----------------
| ✅ Final Answer |
----------------

Retrieval-Augmented Generation (RAG) is an AI architecture that combines information retrieval with large language models. Instead of relying only on the model's internal knowledge, it retrieves relevant external documents and uses them as context to generate more accurate, up-to-date, and grounded responses. This approach improves factual correctness, reduces hallucinations, and enables LLMs to answer domain-specific questions using private knowledge bases.
```

---


y improves both search coverage and response efficiency.