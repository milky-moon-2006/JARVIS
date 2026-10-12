import requests
from config import OLLAMA_URL, AI_MODEL
from core.memory import context
SYSTEM="""You are JARVIS, a polished desktop AI assistant. Be concise, helpful,
calm and professional. You may say sir occasionally. Never claim a computer
action was completed unless the application actually executed it."""
def ask(question):
    prompt=SYSTEM+"\n\nConversation memory:\n"+(context() or "(none)")+"\n\nUSER: "+question+"\nJARVIS:"
    try:
        r=requests.post(OLLAMA_URL,json={"model":AI_MODEL,"prompt":prompt,"stream":False},timeout=120)
        r.raise_for_status()
        return r.json().get("response","").strip() or "I have no response at the moment."
    except requests.exceptions.ConnectionError:
        return "I cannot reach Ollama. Please make sure Ollama is running."
    except Exception as e:
        print("AI ERROR:",e); return "I encountered an AI connection error."
