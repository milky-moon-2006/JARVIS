import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play

load_dotenv("voice/.env")

api_key = os.getenv("ELEVENLABS_API_KEY")

if not api_key:
    raise RuntimeError("ELEVENLABS_API_KEY not found")

client = ElevenLabs(api_key=api_key)

print("JARVIS: Testing ElevenLabs voice...")
print("JARVIS: Generating speech...")

audio = client.text_to_speech.convert(
    text="Hello sir. JARVIS voice system is now online.",
    voice_id="pNInz6obpgDQGcFmaJgB",
    model_id="eleven_multilingual_v2",
    output_format="mp3_22050_32",
)

play(audio)

print("JARVIS: Voice test complete.")