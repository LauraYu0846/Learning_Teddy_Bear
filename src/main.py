from stt import transcribe_live_audio
from assistant import new_session, message, get_context_variables
from translator import translate_language
import utilities
import json
import time

def watson_conversation():
    session_id = new_session()
    for i in range(4):
        if i == 0:
            user_message = ""
        else:
            user_message = transcribe_live_audio(language="english")

        watson_response = message(session_id, user_message)
        utilities.speaker(watson_response)

    return get_context_variables(session_id)


def learn_language(context_variables, question_dict):
    question = utilities.random_question(question_dict, context_variables["difficulty"])[0]

    # speak the question from question bank in english
    utilities.speaker(question)

    answer = transcribe_live_audio(language="english")

    # kids answer the question
    output_language = context_variables["language"].lower()
    text = f"{answer} in {output_language} is"

    # Watson translate the answer
    utilities.speaker(text)

    translated_text = translate_language(answer, output_language)
    utilities.speaker(translated_text, output_language)

    # Tell user to repeat
    utilities.speaker("Please repeat after me")
    time.sleep(5)


    # wait the user to repeat the new language


def main():
    context_variables = watson_conversation()

    with open('questions.json') as questionbank:
        question_dict = json.load(questionbank)

    for i in range(utilities.get_num_questions(context_variables["difficulty"])):
        learn_language(context_variables, question_dict)


# json file to contain all the questions (just created at pycharm)

main()
