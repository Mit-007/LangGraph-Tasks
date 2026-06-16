from app.core.config import GOOGLE_API_KEY
from app.core.constant import OUTPUT_DIMENSIONALITY , TEMPERATURE
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from app.services.logger import logger

def get_llm(llm_model):
    try:

        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is missing. Please set it in your .env file.")

        llm = ChatGoogleGenerativeAI(
            model = llm_model,
            temperature=TEMPERATURE
        )
    except Exception as e:
        llm = None

    return llm 

def get_embeddding_model(model_name):
    try:

        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is missing. Please set it in your .env file.")

        embedding_model = GoogleGenerativeAIEmbeddings(
            model=model_name,
            output_dimensionality=OUTPUT_DIMENSIONALITY
        )

    except Exception as e:
        embedding_model = None

    return embedding_model 



llm = get_llm("gemini-3.1-flash-lite")

llm_DB_researcher = get_llm("gemini-3.1-flash-lite")

llm_Doc_researcher = get_llm("gemini-3.5-flash")

llm_web_researcher = get_llm("gemini-3.1-flash-lite")

embedding_model = get_embeddding_model("models/gemini-embedding-001")