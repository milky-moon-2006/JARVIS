import os
import threading
import tempfile
import subprocess
import speech_recognition as sr
from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(BASE_DIR, "voice", ".env")

load_dotenv(ENV_FILE, override=True)


# ============================================================
# JARVIS VOICE ENGINE
# OPENAI TTS + MICROPHONE
# FEMALE JARVIS VOICE
# ============================================================

# Load .env from the project folder
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(PROJECT_DIR, ".env")

load_dotenv(ENV_FILE)


class VoiceEngine:

    def __init__(self, hud=None):

        self.hud = hud

        # ----------------------------------------------------
        # OpenAI
        # ----------------------------------------------------

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY was not found in the .env file."
            )

        self.client = OpenAI(api_key=api_key)

        # ----------------------------------------------------
        # Speech recognition
        # ----------------------------------------------------

        self.recognizer = sr.Recognizer()

        # Microphone settings
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5

        # ----------------------------------------------------
        # State
        # ----------------------------------------------------

        self.speaking = False
        self.listening = False

        # Prevent multiple voices speaking at once
        self._speak_lock = threading.Lock()

        # ----------------------------------------------------
        # FFmpeg / FFplay
        # ----------------------------------------------------

        self.ffplay = self.find_ffplay()

        if self.ffplay:
            print("✓ FFplay found:")
            print(self.ffplay)
        else:
            print("⚠ FFplay was not found automatically.")

    # ========================================================
    # FIND FFPLAY
    # ========================================================

    def find_ffplay(self):

        # First check PATH
        try:
            result = subprocess.run(
                ["where", "ffplay"],
                capture_output=True,
                text=True,
                check=False
            )

            if result.returncode == 0:
                path = result.stdout.strip().splitlines()[0]

                if os.path.exists(path):
                    return path

        except Exception:
            pass

        # Common locations
        possible_paths = [
            r"D:\ffmpeg-9.0.1-essentials_build\ffmpeg-9.0.1-essentials_build\bin\ffplay.exe",
            r"D:\ffmpeg-9.0.1-essentials_build\bin\ffplay.exe",
            r"C:\ffmpeg\bin\ffplay.exe",
            r"C:\Program Files\ffmpeg\bin\ffplay.exe",
        ]

        for path in possible_paths:

            if os.path.exists(path):
                return path

        return None

    # ========================================================
    # HUD STATUS
    # ========================================================

    def set_status(self, value):

        if self.hud is not None:

            try:
                self.hud.set_status(value)

            except Exception:
                pass

    # ========================================================
    # HUD MESSAGE
    # ========================================================

    def set_message(self, value):

        if self.hud is not None:

            try:
                self.hud.set_message(value)

            except Exception:
                pass

    # ========================================================
    # OPENAI TEXT TO SPEECH
    # FEMALE JARVIS VOICE
    # ========================================================

    def speak(self, message):

        if not message:
            return

        message = str(message).strip()

        if not message:
            return

        # Prevent multiple voices speaking at once
        with self._speak_lock:

            self.speaking = True

            self.set_status("● SPEAKING")
            self.set_message(message)

            print()
            print("JARVIS:", message)
            print("NOVA: Generating female voice...")

            audio_file = None

            try:

                # ------------------------------------------------
                # Create temporary MP3 file
                # ------------------------------------------------

                with tempfile.NamedTemporaryFile(
                    suffix=".mp3",
                    delete=False
                ) as temp:

                    audio_file = temp.name

                # ------------------------------------------------
                # OpenAI TTS
                # ------------------------------------------------

                response = self.client.audio.speech.create(
                    model="gpt-4o-mini-tts",

                    # Female-sounding OpenAI voice
                    voice="coral",

                    input=message,

                    # JARVIS personality
                    instructions=(
                        "Speak in a natural, warm, feminine voice. "
                        "Sound intelligent, calm, confident, elegant, "
                        "professional, and futuristic. "
                        "Speak clearly and naturally like an advanced AI Assistant. "
                        "AI assistant. Do not sound robotic."
                    ),

                    response_format="mp3"
                )

                response.write_to_file(audio_file)

                print("✓ FEMALE JARVIS VOICE GENERATED")

                # ------------------------------------------------
                # Play MP3 using FFplay
                # ------------------------------------------------

                if not self.ffplay:

                    raise RuntimeError(
                        "FFplay was not found. "
                        "Please make sure FFmpeg/FFplay is installed."
                    )

                print("🔊 Playing voice...")

                subprocess.run(
                    [
                        self.ffplay,
                        "-nodisp",
                        "-autoexit",
                        "-loglevel",
                        "quiet",
                        audio_file
                    ],
                    check=False
                )

                print("✓ Voice playback complete")

            except Exception as error:

                print()
                print("NOVA VOICE ERROR:", error)

                self.set_message(
                    "JARVIS voice could not be played."
                )

            finally:

                # ------------------------------------------------
                # Delete temporary audio
                # ------------------------------------------------

                if audio_file:

                    try:

                        if os.path.exists(audio_file):
                            os.remove(audio_file)

                    except Exception:
                        pass

                self.speaking = False

                self.set_status("● SYSTEM ONLINE")

    # ========================================================
    # MICROPHONE CALIBRATION
    # ========================================================

    def calibrate_microphone(self, source):

        print("Calibrating microphone...")

        self.set_status("● CALIBRATING")
        self.set_message("Adjusting microphone...")

        try:

            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=0.6
            )

            print("Microphone ready.")

        except Exception as error:

            print(
                "MIC CALIBRATION ERROR:",
                error
            )

    # ========================================================
    # LISTEN
    # ========================================================

    def listen(
        self,
        timeout=5,
        phrase_time_limit=10
    ):

        # Don't listen while JARVIS is speaking
        if self.speaking:

            print(
                "JARVIS is speaking. "
                "Microphone temporarily paused."
            )

            return ""

        self.listening = True

        self.set_status("● LISTENING")
        self.set_message("Listening...")

        print()
        print("🎤 Listening...")

        try:

            with sr.Microphone() as source:

                # --------------------------------------------
                # Microphone calibration
                # --------------------------------------------

                self.calibrate_microphone(source)

                self.set_status("● LISTENING")

                self.set_message(
                    "Listening for your command..."
                )

                # --------------------------------------------
                # Listen
                # --------------------------------------------

                try:

                    audio = self.recognizer.listen(
                        source,
                        timeout=timeout,
                        phrase_time_limit=phrase_time_limit
                    )

                except sr.WaitTimeoutError:

                    print("Listening timed out.")

                    return ""

        except Exception as error:

            print()
            print(
                "MICROPHONE ERROR:",
                error
            )

            self.set_status("● SYSTEM ONLINE")

            self.set_message(
                "Microphone unavailable."
            )

            return ""

        finally:

            self.listening = False

        # ====================================================
        # SPEECH RECOGNITION
        # ====================================================

        self.set_status("● THINKING")
        self.set_message("Understanding...")

        print()
        print("🔄 Understanding...")

        try:

            result = self.recognizer.recognize_google(
                audio
            )

            result = result.lower().strip()

            print()
            print("YOU:", result)

            self.set_message(result)

            self.set_status("● SYSTEM ONLINE")

            return result

        except sr.UnknownValueError:

            print(
                "Could not understand speech."
            )

            self.set_status("● SYSTEM ONLINE")

            self.set_message(
                "I couldn't understand that."
            )

            return ""

        except sr.RequestError as error:

            print()
            print(
                "Speech recognition service error:",
                error
            )

            self.set_status("● SYSTEM ONLINE")

            self.set_message(
                "Speech recognition unavailable."
            )

            return ""

        except Exception as error:

            print()
            print(
                "RECOGNITION ERROR:",
                error
            )

            self.set_status("● SYSTEM ONLINE")

            self.set_message(
                "Recognition error."
            )

            return ""

    # ========================================================
    # SAFE LISTEN
    # ========================================================

    def listen_safely(
        self,
        timeout=5,
        phrase_time_limit=10
    ):

        try:

            return self.listen(
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )

        except Exception as error:

            print()
            print(
                "SAFE LISTEN ERROR:",
                error
            )

            self.set_status("● SYSTEM ONLINE")

            return ""


# ============================================================
# VOICE ENGINE TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("======================================")
    print("      JARVIS VOICE ENGINE TEST")
    print("      FEMALE JARVIS VOICE")
    print("======================================")
    print()

    try:

        voice = VoiceEngine()

        # ----------------------------------------------------
        # Test female voice
        # ----------------------------------------------------

        voice.speak(
            "Hello sir. My voice system is ready. "
            "I am JARVIS, and I am now online."
        )

        print()

        print("======================================")
        print(" MICROPHONE TEST")
        print("======================================")
        print()

        # ----------------------------------------------------
        # Test microphone
        # ----------------------------------------------------

        text = voice.listen_safely(
            timeout=5,
            phrase_time_limit=10
        )

        print()

        print("Recognized:")
        print(text)

    except Exception as error:

        print()
        print("======================================")
        print("JARVIS VOICE ENGINE ERROR")
        print("======================================")
        print(error)