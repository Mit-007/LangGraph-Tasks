from app.core.config import GOOGLE_API_KEY
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0
)

llm_DB_researcher = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0
)

llm_Doc_researcher = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0
)   

llm_web_researcher = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0
)   

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    output_dimensionality=3072
)
