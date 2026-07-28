import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing in .env")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env")