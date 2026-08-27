import os
from dotenv import load_dotenv

load_dotenv()

# Local OpenAI-compatible inference server.
# Default: Ollama running on the same device.
AI_BASE_URL = os.getenv("AI_BASE_URL", "http://127.0.0.1:11434/v1")
AI_MODEL = os.getenv("AI_MODEL", "llama3.2:3b")

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
