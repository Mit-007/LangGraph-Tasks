from dotenv import load_dotenv
import os
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
TAVILY_API_KEY=os.getenv("TAVILY_API_KEY")
INDEX_NAME=os.getenv("INDEX_NAME")