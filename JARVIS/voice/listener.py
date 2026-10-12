import speech_recognition as sr
from config import LISTEN_TIMEOUT, PHRASE_TIME_LIMIT, WAKE_WORDS
_recognizer=sr.Recognizer()
def listen():
    try:
        with sr.Microphone() as source:
            print("Listening..."); _recognizer.adjust_for_ambient_noise(source,duration=.4)
            audio=_recognizer.listen(source,timeout=LISTEN_TIMEOUT,phrase_time_limit=PHRASE_TIME_LIMIT)
        text=_recognizer.recognize_google(audio).lower().strip(); print("YOU:",text); return text
    except sr.WaitTimeoutError: return ""
    except sr.UnknownValueError: print("I did not understand that.")
    except sr.RequestError: print("Speech recognition service is unavailable.")
    except Exception as e: print("MIC ERROR:",e)
    return ""
def wake_word_detected(text):
    t=text.lower().strip(); return any(w in t for w in WAKE_WORDS)
def listen_for_wake_word():
    text=listen(); return bool(text and wake_word_detected(text))
