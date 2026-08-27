import os
from dotenv import load_dotenv

load_dotenv()

# MI-IA Engine is the default inference backend.
AI_BASE_URL = os.getenv("AI_BASE_URL", "http://127.0.0.1:8080/v1")
AI_MODEL = os.getenv("AI_MODEL", "miia-local")

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
