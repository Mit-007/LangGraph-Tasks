from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import GOOGLE_API_KEY
from app.utils.logger import logger

def call_llm():
    try :
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is missing. Please set it in your .env file.")

        return ChatGoogleGenerativeAI(
            model="gemini-3.1-flash-lite",
            temperature=0
        )
    
    except Exception as e:

        logger.error(f"Error in call_llm: {e}")

        return None
