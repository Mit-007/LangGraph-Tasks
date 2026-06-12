# 🗄️ Database Research Agent

A specialized **LangGraph-based database research agent** that performs **parallel SQLite database querying** by breaking a user's question into multiple SQL sub-queries, executing them concurrently on a **SQLite database**, and synthesizing the results into a single comprehensive answer.

Before query planning begins, the agent first retrieves the **database schema**, enabling the LLM to generate accurate SQL queries based on the available tables and columns.

The agent follows a **Schema Retrieval → Orchestrator → Worker → Aggregator** architecture to improve query accuracy and reduce execution latency through parallel processing.

---

# 📖 Project Overview

The Database Research Agent is designed to answer natural language questions using structured data stored in a **SQLite database**.

Instead of generating a single SQL query for a complex question, the agent:

* retrieves the SQLite database schema,
* analyzes the user's question,
* generates multiple SQL sub-queries,
* executes them in parallel,
* collects the results,
* and produces one well-structured final response.

This architecture enables efficient handling of complex analytical questions while maintaining modularity and scalability.

---

# ✨ Features

* ✅ Automatic SQLite schema retrieval
* ✅ Intelligent SQL query decomposition
* ✅ Parallel SQL execution
* ✅ Multi-node LangGraph workflow
* ✅ LLM-powered SQL generation
* ✅ Automatic answer synthesis
* ✅ Modular architecture
* ✅ Independent runnable agent

---

# 🏗️ Architecture

<img width="243" height="531" alt="DB_researcher" src="https://github.com/user-attachments/assets/8dc66a24-53f5-4c7f-95c2-70924468b07e" />

---

# ⚙️ How the Agent Works

The agent processes a user query through four major stages.

---

## 1️⃣ Schema Retrieval Node

Before generating any SQL queries, the workflow first retrieves the schema of the connected **SQLite database**.

Its responsibilities include:

* Reading available tables
* Reading table columns
* Extracting schema metadata
* Preparing schema context for the LLM

Providing the schema beforehand allows the LLM to generate valid SQL queries based on the actual database structure.

The retrieved schema is then passed to the Orchestrator node.

---

## 2️⃣ Orchestrator Node

The Orchestrator acts as the planner of the workflow.

Its responsibilities include:

* Receiving the user's question
* Understanding the analytical objective
* Using the retrieved database schema as context
* Breaking the question into multiple SQL sub-queries
* Preparing database tasks for parallel execution

Rather than generating one large SQL statement, the orchestrator decomposes complex problems into smaller independent SQL queries.

These SQL queries are then forwarded to the Worker node.

---

## 3️⃣ Worker Node

The Worker node is responsible for executing all generated SQL queries.

Each SQL query is processed independently and **in parallel**, allowing multiple database operations to execute simultaneously.

The Worker performs the following tasks:

* Receives generated SQL queries
* Connects to the local SQLite database file
* Executes SQL statements using Python's built-in `sqlite3` library
* Retrieves query results
* Returns structured outputs to the Aggregator

Since all database queries execute concurrently, the overall execution time is significantly reduced.

Each worker remains independent and focuses solely on SQL execution.

---

## 4️⃣ Aggregator Node

The Aggregator receives outputs from all parallel workers.

Its responsibilities include:

* Collecting SQL execution results
* Combining related outputs
* Interpreting numerical and tabular data
* Removing redundant information
* Generating a coherent natural language response

The final output is a single synthesized answer generated from the executed SQL queries.

---

# 🔄 Workflow

```text
                 User Question
                        │
                        ▼
              ┌──────────────────┐
              │ Retrieve Schema  │
              └──────────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │   Orchestrator   │
              └──────────────────┘
                        │
         Generates Multiple SQL Queries
                        │
                        ▼
────────────────────────────────────────────
│          │            │          │
▼          ▼            ▼          ▼
SQL       SQL         SQL        SQL
Query 1   Query 2     Query 3    Query N
│          │            │          │
▼          ▼            ▼          ▼
Execute   Execute     Execute    Execute
Query     Query       Query      Query
│          │            │          │
└──────────┴────────────┴──────────┘
            Parallel Execution
                        │
                        ▼
              ┌──────────────────┐
              │    Aggregator    │
              └──────────────────┘
                        │
                        ▼
              Final Synthesized Answer
```

---

# 🛠️ Tech Stack

| Technology          | Purpose                          |
| ------------------- | -------------------------------- |
| Python              | Programming Language             |
| LangGraph           | Workflow Orchestration           |
| LangChain           | LLM Integration                  |
| SQLite (`sqlite3`)  | Local Relational Database        |
| SQL                 | Query Language                   |
| Google Gemini / LLM | SQL Planning & Answer Generation |

---

# 🗃️ Database

This project uses a **local SQLite database** as its structured data source.

Before generating SQL queries, the agent automatically retrieves the database schema and uses it as context for the LLM.

Example database path:

```text
app/db/Task_3_data.db
```

Because SQLite is a file-based database, the project can run without installing or configuring an external database server such as MySQL or PostgreSQL.

---

# ▶️ Running the Agent

Open a terminal.

```bash
cd Task-3
```

Run the Database Research Agent:

```bash
python -m app.main_DB
```

The agent will execute the complete database research workflow and generate a synthesized response.

---

# 🔑 Environment Setup

This agent uses a **local SQLite database**, so no external database server is required.

Configure your LLM API key in the `.env` file:

```env
GOOGLE_API_KEY="your_google_api_key"
```

**Notes :The SQLite database file ( `app/db/Task_3_data.db`) should already exist and contain the your required tables and sample data.
so upload data Into this file only.
**

> **Note:** Since SQLite is a file-based database, no additional database installation or configuration is needed.

For complete environment setup instructions and API key configuration, please refer to the **root `README.md`** of the project.

---

# 📤 Example Output

```text
-----------------
| 👨 Query      |
-----------------

How many total employees are?

------------------
| 📋 Sub Queries |
------------------

[
  Db_query_schema(
      query_name='total_employees',
      query='SELECT count(*) FROM employees;'
  )
]

--------------------
| 👷 Worker Output |
--------------------

[
  {
    'sub_query':
      Db_query_schema(
        query_name='total_employees',
        query='SELECT count(*) FROM employees;'
      ),

    'db_path':'app/db/Task_3_data.db',

    'result':[(5,)]
  }
]

-------------------
| ✅ Final Answer |
-------------------

There are a total of **5 employees** in the database.
```

---

