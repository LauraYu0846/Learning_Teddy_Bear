import os
from dotenv import load_dotenv

load_dotenv()

stt_key = os.environ.get("STT_KEY")
stt_url = os.environ.get("STT_URL")