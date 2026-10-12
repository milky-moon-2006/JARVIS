






import threading
from core.ai import ask
from core.memory import add,clear
from core.router import handle
from core.security import is_exit
from voice.listener import listen
from voice.speaker import speak
def process_command(command):
    if not command: return True
    command=command.strip()
    if is_exit(command): speak("Goodbye, sir."); return False
    if command.lower() in {"clear memory","forget conversation","forget our conversation"}:
        clear(); speak("Conversation memory has been cleared."); return True
    result=handle(command)
    if result is not None:
        add("user",command); add("assistant",result); speak(result); return True
    add("user",command); answer=ask(command); add("assistant",answer); speak(answer); return True
def voice_command():
    text=listen()
    if text: process_command(text)
def run_jarvis():
    speak("JARVIS is online. All systems are ready.")
    threading.Event().wait()
