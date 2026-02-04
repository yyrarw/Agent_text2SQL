from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[1]

load_dotenv(BASE_DIR / ".env")

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL")
    OPENAI_TEMPERATURE = os.getenv("OPENAI_TEMPERATURE")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
