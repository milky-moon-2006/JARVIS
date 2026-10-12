import pyttsx3
from config import VOICE_RATE, VOICE_VOLUME
_engine=None
def speak(text):
    global _engine
    if not text: return
    print("JARVIS:",text)
    try:
        if _engine is None:
            _engine=pyttsx3.init(); _engine.setProperty("rate",VOICE_RATE); _engine.setProperty("volume",VOICE_VOLUME)
            for voice in _engine.getProperty("voices"):
                if "zira" in getattr(voice,"name","").lower():
                    _engine.setProperty("voice",voice.id); break
        _engine.say(str(text)); _engine.runAndWait()
    except Exception as e: print("TTS ERROR:",e)
