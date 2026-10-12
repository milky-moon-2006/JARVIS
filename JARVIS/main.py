import pyttsx3
import speech_recognition as sr
import requests
import webbrowser
import subprocess
import urllib.parse
import json
import pywhatkit


OLLAMA_URL = "http://localhost:11434/api/generate"
AI_MODEL = "llama3.2:1b"
CONTACT_FILE = "contacts.json"


# ==============================
# VOICE
# ==============================

def speak(text):

    if not text:
        return

    print("\nJARVIS:", text)

    try:

        engine = pyttsx3.init()

        voices = engine.getProperty("voices")

        for voice in voices:

            if "Zira" in voice.name:

                engine.setProperty(
                    "voice",
                    voice.id
                )

                break

        engine.setProperty("rate", 175)
        engine.setProperty("volume", 1.0)

        engine.say(str(text))
        engine.runAndWait()
        engine.stop()

    except Exception as error:

        print("VOICE ERROR:", error)


# ==============================
# MICROPHONE
# ==============================

def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("\n🎤 Listening...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.5
        )

        try:

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        except sr.WaitTimeoutError:

            return ""

    try:

        print("🔄 Understanding...")

        text = recognizer.recognize_google(audio)

        print("YOU:", text)

        return text.lower().strip()

    except sr.UnknownValueError:

        speak("Sorry, I didn't understand.")

        return ""

    except sr.RequestError:

        speak("Speech recognition is unavailable.")

        return ""


# ==============================
# LOCAL AI
# ==============================

def ask_ai(question):

    print("\n🧠 Asking local AI...")

    try:

        data = {
            "model": AI_MODEL,
            "prompt": question,
            "stream": False
        }

        response = requests.post(
            OLLAMA_URL,
            json=data,
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        answer = result.get(
            "response",
            ""
        ).strip()

        print("\nAI ANSWER:")
        print(answer)

        return answer

    except Exception as error:

        print("AI ERROR:", error)

        return "Sorry Ayan, I could not get an AI answer."


# ==============================
# WHATSAPP
# ==============================

def send_whatsapp(contact_name, message):

    try:

        with open(
            CONTACT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            contacts = json.load(file)

    except Exception:

        speak("I cannot open your contacts file.")

        return


    phone_number = None

    for name, number in contacts.items():

        if name.lower() == contact_name.lower():

            phone_number = number

            break


    if phone_number is None:

        speak(
            "I could not find "
            + contact_name
            + " in your contacts."
        )

        return


    speak(
        "You want me to send "
        + message
        + " to "
        + contact_name
        + "."
    )


    confirmation = input(
        "Type YES to send the message: "
    ).strip().lower()


    if confirmation != "yes":

        speak("Message cancelled.")

        return


    speak("Opening WhatsApp.")

    try:

        pywhatkit.sendwhatmsg_instantly(
            phone_number,
            message,
            wait_time=15,
            tab_close=True
        )

        speak("WhatsApp message sent.")

    except Exception as error:

        print("WHATSAPP ERROR:", error)

        speak(
            "Sorry, I could not send the WhatsApp message."
        )


# ==============================
# COMMANDS
# ==============================

def handle_command(command):

    command = command.lower().strip()


    # ==========================
    # YOUTUBE
    # ==========================

    if command == "open youtube":

        speak("Opening YouTube.")

        webbrowser.open(
            "https://www.youtube.com"
        )

        return True


    # ==========================
    # GOOGLE
    # ==========================

    if command == "open google":

        speak("Opening Google.")

        webbrowser.open(
            "https://www.google.com"
        )

        return True


    # ==========================
    # OPENAI
    # ==========================

    if command in [
        "open openai",
        "open chatgpt"
    ]:

        speak("Opening OpenAI.")

        webbrowser.open(
            "https://chatgpt.com"
        )

        return True


    # ==========================
    # GEMINI
    # ==========================

    if command == "open gemini":

        speak("Opening Gemini.")

        webbrowser.open(
            "https://gemini.google.com"
        )

        return True


    # ==========================
    # WHATSAPP
    # ==========================

    if command == "open whatsapp":

        speak("Opening WhatsApp.")

        webbrowser.open(
            "https://web.whatsapp.com"
        )

        return True


    # ==========================
    # CHROME
    # ==========================

    if command == "open chrome":

        speak("Opening Chrome.")

        try:

            subprocess.Popen(
                [
                    "cmd",
                    "/c",
                    "start",
                    "",
                    "chrome"
                ]
            )

        except Exception:

            speak(
                "I could not open Chrome."
            )

        return True


    # ==========================
    # VS CODE
    # ==========================

    if command in [
        "open vs code",
        "open vscode"
    ]:

        speak(
            "Opening Visual Studio Code."
        )

        try:

            subprocess.Popen(
                ["code"]
            )

        except Exception:

            speak(
                "I could not open Visual Studio Code."
            )

        return True


    # ==========================
    # GOOGLE SEARCH
    # ==========================

    if command.startswith(
        "search google for "
    ):

        search_text = command.replace(
            "search google for ",
            "",
            1
        ).strip()


        if search_text:

            speak(
                "Searching Google for "
                + search_text
            )

            url = (
                "https://www.google.com/search?q="
                + urllib.parse.quote(search_text)
            )

            webbrowser.open(url)


        return True


    # ==========================
    # YOUTUBE SEARCH
    # ==========================

    if command.startswith(
        "search youtube for "
    ):

        search_text = command.replace(
            "search youtube for ",
            "",
            1
        ).strip()


        if search_text:

            speak(
                "Searching YouTube for "
                + search_text
            )

            url = (
                "https://www.youtube.com/results?search_query="
                + urllib.parse.quote(search_text)
            )

            webbrowser.open(url)


        return True


    # ==========================
    # WHATSAPP MESSAGE
    # ==========================

    if command.startswith(
        "send whatsapp to "
    ):

        remaining = command.replace(
            "send whatsapp to ",
            "",
            1
        ).strip()


        if " saying " not in remaining:

            speak(
                "Please say: "
                "send whatsapp to contact "
                "saying message."
            )

            return True


        contact_name, message = remaining.split(
            " saying ",
            1
        )


        send_whatsapp(
            contact_name.strip(),
            message.strip()
        )

        return True


    # ==========================
    # LOCK LAPTOP
    # ==========================

    if command in [
        "lock my laptop",
        "lock laptop",
        "lock computer"
    ]:

        speak(
            "Locking your laptop."
        )

        subprocess.run(
            [
                "rundll32.exe",
                "user32.dll",
                "LockWorkStation"
            ]
        )

        return True


    # ==========================
    # SHUTDOWN LAPTOP
    # ==========================

    if command in [
        "shutdown my laptop",
        "shutdown laptop",
        "shutdown computer",
        "turn off my laptop"
    ]:

        speak(
            "Are you sure you want "
            "to shut down your laptop?"
        )


        confirmation = input(
            "Type YES to shut down: "
        ).strip().lower()


        if confirmation == "yes":

            speak(
                "Shutting down your laptop "
                "in ten seconds."
            )

            subprocess.run(
                [
                    "shutdown",
                    "/s",
                    "/t",
                    "10"
                ]
            )

        else:

            speak(
                "Shutdown cancelled."
            )


        return True


    return False


# ==============================
# START JARVIS
# ==============================

speak(
    "Hello Ayan. "
    "I am Jarvis. "
    "Your local AI assistant is ready."
)


# ==============================
# MAIN LOOP
# ==============================

while True:

    print("\n================================")
    print("           JARVIS V1")
    print("================================")
    print("Press ENTER to speak.")
    print("Or type a command.")
    print("Type exit to stop.")
    print("================================")


    typed = input("\nYou: ")


    if typed.strip():

        question = typed.strip()

    else:

        question = listen()


    if question.lower() in [
        "exit",
        "quit",
        "stop jarvis"
    ]:

        speak("Goodbye Ayan.")

        break


    if not question:

        continue


    if handle_command(question):

        continue


    answer = ask_ai(question)

    speak(answer)