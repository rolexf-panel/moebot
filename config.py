import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:14b")
DB_PATH = os.getenv("DB_PATH", "moebot.db")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "20"))
FLOOD_THRESHOLD = int(os.getenv("FLOOD_THRESHOLD", "5"))
FLOOD_COOLDOWN = int(os.getenv("FLOOD_COOLDOWN", "300"))

ADMINS = set()
