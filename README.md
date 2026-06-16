# Multi-Task Project

This repository contains four independent tasks/projects.

## Project Structure

<img width="375" height="358" alt="Screenshot 2026-06-11 214024" src="https://github.com/user-attachments/assets/52c7febc-1b15-4fcc-b5b4-1efd4423964d" />

---

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
---

## 🔑 Environment Variables & API Setup

Before running this project, you need to configure the required API keys and create a `.env` file in the project root.

### Environment Variables

```env
GOOGLE_API_KEY="xxxxxx"
PINECONE_API_KEY="xxxxxx"
TAVILY_API_KEY="xxxxxx"
INDEX_NAME="Your_index_name"
DB_PATH_OF_COLLECTION_TASK_3 =  "app/db/Task_3_data.db"
DB_PATH_OF_CHAT_HISTORY_TASK_3 = "app/db/agent_history.db"
DB_PATH_OF_CHAT_HISTORY_TASK_4 = "app/db/agent_history.db" 
```

### 1️⃣ Google API Key (Gemini)

This project uses Google's Gemini models for LLM-based reasoning.

#### Steps to generate:

1. Visit **https://aistudio.google.com/**
2. Sign in with your Google account.
3. Click **Get API Key**.
4. Create a new API key.
5. Copy the generated key.
6. Paste it into:

```env
GOOGLE_API_KEY="your_google_api_key"
```

---

### 2️⃣ Pinecone API Key

Pinecone is used as the vector database for storing and retrieving embeddings.

#### Steps to generate:

1. Visit **https://app.pinecone.io/**
2. Create an account or sign in.
3. Navigate to **API Keys**.
4. Create or copy your API key.
5. Add it to your `.env` file.

```env
PINECONE_API_KEY="your_pinecone_api_key"
```

---

### 3️⃣ Create a Pinecone Index

After logging into Pinecone:

1. Go to **Indexes**.
2. Click **Create Index**.
3. Provide an index name (for example: `research-agent`).
4. Select the embedding dimension matching your embedding model.
5. Wait for the index to be created.
6. Upload your document embeddings to this index.
7. Set the same index name in your `.env` file.

```env
INDEX_NAME="research-agent"
```

> **Note:** IN Task-3 The Document research agents expect your vector data to already be uploaded into the specified Pinecone index.

---

### 4️⃣ Tavily API Key

Tavily is used by the Web Research Agent for real-time web search.

#### Steps to generate:

1. Visit **https://app.tavily.com/**
2. Sign up or log in.
3. Navigate to the dashboard.
4. Generate an API key.
5. Copy the key and add it to your `.env` file.

```env
TAVILY_API_KEY="your_tavily_api_key"
```
> **Note:** Use In Task - 3 for web Search . 
---


# Running Individual Tasks

> **Important:** Before running any specific task, please read the `README.md` file inside that task's folder. Each task contains detailed information about its purpose, project structure, functionality, and execution instructions. This will help you better understand the sub-project and how to run it correctly.

## Task-1

Navigate to the task folder:

```bash
cd Task-1
```

Run the application:

```bash
python -m app.main
```

---

## Task-2

Navigate to the task folder:

```bash
cd Task-2
```

Run the application:

```bash
python -m app.main
```

---

## Task-3

Navigate to the task folder:

```bash
cd Task-3
```

Run the application:

```bash
python -m app.main
```

---

## Task-4

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

## Requirements

All project dependencies are listed in:

```text
requirements.txt
```

Install them before running any task.

---

## Notes

* Ensure Python 3.10+ is installed.
* Activate the virtual environment before running any task.
* Configure the required API keys in the `.env` file before running the applications.
* Read the task-specific `README.md` before running a particular task.
* Each task is independent and can be executed separately.
* Task-4 exposes REST APIs through FastAPI and provides interactive API documentation using Swagger UI.
