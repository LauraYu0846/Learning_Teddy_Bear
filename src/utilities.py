import random
import json
from tts import text_to_audio, play_audio_file


def random_question(difficulty):
    with open('questions.json') as questionbank:
        q = json.load(questionbank)
    return random.choice(list(q[difficulty].values()))


def speaker(text):
    text_to_audio(text)
    play_audio_file()