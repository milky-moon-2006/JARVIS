from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MEMORY_FILE = DATA_DIR / "memory.json"
CONTACTS_FILE = DATA_DIR / "contacts.json"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
AI_MODEL = "llama3.2:1b"
WAKE_WORDS = ("hey jarvis", "hey jervis", "jarvis")
LISTEN_TIMEOUT = 5
PHRASE_TIME_LIMIT = 10
VOICE_RATE = 175
VOICE_VOLUME = 1.0
