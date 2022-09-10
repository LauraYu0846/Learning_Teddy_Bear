import os
from dotenv import load_dotenv

load_dotenv()

stt_key = os.environ.get("STT_KEY")
stt_url = os.environ.get("STT_URL")

tts_key = os.environ.get("TTS_KEY")
tts_url = os.environ.get("TTS_URL")

lt_key = os.environ.get("LT_KEY")
lt_url = os.environ.get("LT_URL")

assistant_key = os.environ.get("ASSISTANT_KEY")
assistant_url = os.environ.get("ASSISTANT_URL")
assistant_id = os.environ.get("ASSISTANT_ID")

