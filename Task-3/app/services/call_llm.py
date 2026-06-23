from app.core.config import GOOGLE_API_KEY
from app.core.constant import OUTPUT_DIMENSIONALITY , TEMPERATURE
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from app.services.logger import logger


#  -> provide embedding model for Query Embedding.
def embedding_model():
    try:

        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is missing. Please set it in your .env file.")

        embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            output_dimensionality=OUTPUT_DIMENSIONALITY
        )

    except Exception as e:
        logger.error(f"can not get embedding Model , {e}")
        embedding_model = None

    return embedding_model 

#  -> provides LLM models.
def llm():
    try:

        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is missing. Please set it in your .env file.")

        llm = ChatGoogleGenerativeAI(
            model = "gemini-3.1-flash-lite",
            temperature=TEMPERATURE
        )
    except Exception as e:
        logger.error(f"can not get llm_Model , {e}")
        llm = None

    return llm 

def llm_DB_researcher():
    try:

        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is missing. Please set it in your .env file.")

        llm = ChatGoogleGenerativeAI(
            model = "gemini-3.1-flash-lite",
            temperature=TEMPERATURE
        )
    except Exception as e:
        logger.error(f"can not get DB_llm_Model , {e}")
        llm = None

    return llm 

def llm_web_researcher():
    try:

        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is missing. Please set it in your .env file.")

        llm = ChatGoogleGenerativeAI(
            model = "gemini-3.1-flash-lite",
            temperature=TEMPERATURE
        )
    except Exception as e:
        logger.error(f"can not get web_llm_Model , {e}")
        llm = None

    return llm 

def llm_Doc_researcher():
    try:

        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is missing. Please set it in your .env file.")

        llm = ChatGoogleGenerativeAI(
            model = "gemini-3.5-flash",
            temperature=TEMPERATURE
        )
    except Exception as e:
        logger.error(f"can not get Doc_llm_Model , {e}")
        llm = None

    return llm 

