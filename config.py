import os
from dotenv import load_dotenv

load_dotenv()

# Load configuration from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATA_DIR = os.getenv("DATA_DIR")
CHROMADB_PATH = os.getenv("CHROMADB_PATH")
