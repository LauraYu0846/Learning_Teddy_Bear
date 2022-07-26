import random
import json
from tts import text_to_audio, play_audio_file


def get_num_questions(difficulty):
    with open('questions.json') as questionbank:
        q = json.load(questionbank)
    return len(q[difficulty])




def random_question(question_dict, difficulty):
    delete_key = random.choice(list(question_dict[difficulty].keys()))
    question = question_dict[difficulty][delete_key]
    question_dict[difficulty].pop(delete_key)
    return question, question_dict


def speaker(text, language="english"):
    text_to_audio(text, language)
    play_audio_file()
