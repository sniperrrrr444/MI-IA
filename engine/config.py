import os
from dotenv import load_dotenv

load_dotenv()

MODEL_PATH = os.getenv("MIIA_MODEL_PATH", "")
HOST = os.getenv("MIIA_HOST", "127.0.0.1")
PORT = int(os.getenv("MIIA_PORT", "8080"))
MAX_NEW_TOKENS = int(os.getenv("MIIA_MAX_NEW_TOKENS", "512"))
TEMPERATURE = float(os.getenv("MIIA_TEMPERATURE", "0.7"))
