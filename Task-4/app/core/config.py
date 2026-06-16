from dotenv import load_dotenv
import os
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DB_PATH_OF_CHAT_HISTORY = os.getenv("DB_PATH_OF_CHAT_HISTORY_TASK_4")