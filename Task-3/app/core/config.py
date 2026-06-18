from dotenv import load_dotenv
import os
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
TAVILY_API_KEY=os.getenv("TAVILY_API_KEY")
INDEX_NAME=os.getenv("INDEX_NAME")

# ->provide path of SQLite DB for Data Fetch  
DB_PATH_OF_COLLECTION=os.getenv("DB_PATH_OF_COLLECTION_TASK_3")

# ->provide path of SQLite DB for Store History of Graph
DB_PATH_OF_CHAT_HISTORY=os.getenv("DB_PATH_OF_CHAT_HISTORY_TASK_3")