# 📄 Document Research Agent

A specialized **LangGraph-based document research agent** that performs **parallel document retrieval** by breaking a user's query into multiple sub-queries, retrieving relevant document chunks from a **Pinecone vector database**, and synthesizing the retrieved information into a single comprehensive answer.

The agent follows an **Orchestrator → Worker → Aggregator** architecture to improve retrieval quality and reduce response latency through parallel processing.

---

# 📖 Project Overview

The Document Research Agent is designed to answer questions using a collection of **pre-uploaded documents stored in a Pinecone vector database**.

Instead of retrieving information for the entire question at once, the agent:

* analyzes the user's question,
* generates multiple sub-queries,
* executes document retrieval tasks in parallel,
* collects relevant document chunks,
* and produces one well-structured final response.

This parallel retrieval strategy increases document coverage while improving overall execution efficiency.

---

# ✨ Features

* ✅ Intelligent query decomposition
* ✅ Parallel document retrieval
* ✅ Pinecone vector database integration
* ✅ Embedding-based semantic search
* ✅ Multi-node LangGraph workflow
* ✅ Automatic answer synthesis
* ✅ Modular architecture
* ✅ Independent runnable agent

---

# 🏗️ Architecture

<img width="249" height="432" alt="doc_researcher" src="https://github.com/user-attachments/assets/8ea5e996-a417-4009-b156-c814de78fe80" />

---

# ⚙️ How the Agent Works

The agent processes a user query through three major stages.

## 1️⃣ Orchestrator Node

The Orchestrator acts as the planner of the workflow.

Its responsibilities include:

* Receiving the user's query
* Understanding the research objective
* Breaking the query into multiple independent sub-queries
* Preparing retrieval tasks for parallel execution

Rather than retrieving documents for the complete question, the orchestrator decomposes it into smaller semantic search queries that can retrieve more focused document chunks.

These sub-queries are then forwarded to the Worker node.

---

## 2️⃣ Worker Node

The Worker node is responsible for retrieving relevant information from the document knowledge base.

Each sub-query is processed independently and **in parallel**, allowing multiple retrieval operations to execute simultaneously.

it performs the following steps:

* Converts each sub-query into embeddings
* Searches the Pinecone vector database
* Retrieves the most semantically similar document chunks
* Returns the retrieved context to the Aggregator

Each worker focuses only on retrieving relevant information from the document store.

The Pinecone index is expected to contain **pre-uploaded document embeddings**.

---

## 3️⃣ Aggregator Node

The Aggregator receives all retrieved document contexts from the parallel workers.

Its responsibilities include:

* Collecting retrieved document chunks
* Removing duplicate information
* Combining related contexts
* Organizing the information logically
* Using the LLM to generate a coherent final answer based on the retrieved context

The final output is a single synthesized response generated from the relevant document content.

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
Embed     Embed       Embed      Embed
Query 1   Query 2     Query 3    Query N
│          │            │          │
▼          ▼            ▼          ▼
Retrieve  Retrieve    Retrieve   Retrieve
Chunks    Chunks      Chunks     Chunks
│          │            │          │
└──────────┴────────────┴──────────┘
             Parallel Retrieval
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
| Pinecone            | Vector Database                    |
| Embedding Model     | Semantic Search                    |
| Google Gemini / LLM | Query Planning & Answer Generation |

---

# ▶️ Running the Agent

Open a terminal.

```bash
cd Task-3
```

Run the Document Research Agent:

```bash
python -m app.main_Doc
```

The agent will execute the complete document retrieval workflow and generate a synthesized response.

---

# 🔑 Environment Setup

The Document Research Agent requires a **Pinecone API Key** and an existing **Pinecone Index** containing pre-uploaded document embeddings.

Environment configuration:

```env
PINECONE_API_KEY="your_api_key"
INDEX_NAME="your_index_name"
```

**Note:** for upload documents in pinecone always use a given embedding Model:

```
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    output_dimensionality=3072
)
```


> **Note:** The specified Pinecone index must already contain your uploaded document embeddings. The agent retrieves information directly from this existing vector database.

For complete environment setup instructions, API key generation steps, index creation, and `.env` configuration, please refer to the **root `README.md`** of the project.

---

# 📤 Example Output

```
----------------
| 🎯 Topic      |
----------------

Explain Binary Search Tree.

----------------
| 🧩 Sub Topics |
----------------

• Definition of BST
• BST Properties
• BST Operations
• BST Time Complexity
• BST Applications

----------------
| ✅ Final Answer |
----------------

A Binary Search Tree (BST) is a hierarchical data structure in which each node contains a value greater than all values in its left subtree and smaller than all values in its right subtree. This property enables efficient searching, insertion, and deletion operations with an average time complexity of O(log n). BSTs are widely used for implementing ordered collections, indexing systems, and efficient lookup operations.
```

---

