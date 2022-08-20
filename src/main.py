from stt import transcribe_live_audio, activate, stop_program
from assistant import new_session, message
from translator import translate_language
from playmusic import play_music_randomly
from playstory import play_story_randomly
import utilities
import json
import time
from threading import Thread


def watson_conversation():
    session_id = new_session()

    # list_of_options = [
    #     ["english", "spanish", "french"], ["one", "two", "three"]
    # ]

    first_message = True
    context_variables = False
    while not context_variables:
        if first_message:
            user_message = ""
            first_message = False
        else:
            user_message = transcribe_live_audio(language="english")
        watson_response, context_variables = message(session_id, user_message)
        utilities.speaker(watson_response)

    return context_variables


def learn_language(context_variables, question_dict):
    question = utilities.random_question(question_dict, context_variables["difficulty"])[0]

    # speak the question from question bank in english_song
    utilities.speaker(question)

    answer = transcribe_live_audio(language="english")

    # kids answer the question
    output_language = context_variables["language"]
    text = f"{answer} in {output_language} is"

    # Watson translate the answer
    utilities.speaker(text)

    translated_text = translate_language(answer, output_language)
    utilities.speaker(translated_text, output_language)

    # Tell user to repeat
    utilities.speaker("Please repeat after me")
    time.sleep(5)

    # Checking the answer is correct
    user_answer = transcribe_live_audio(language=output_language)

    count = 0
    print("translated text:", translated_text)
    while user_answer != translated_text and count < 3:
        utilities.speaker(translated_text, output_language)
        user_answer = transcribe_live_audio(language=output_language)
        count += 1
        print(user_answer, count)


def main():
    start_program()

    context_variables = watson_conversation()
    print(context_variables)

    if context_variables['activity'] == "language":
        with open('questions.json') as questionbank:
            question_dict = json.load(questionbank)

        for i in range(utilities.get_num_questions(context_variables["difficulty"])):
            learn_language(context_variables, question_dict)

    elif context_variables['activity'] == "music":
        Thread(target=stop_program).start()
        Thread(target=play_music_randomly, args=[context_variables["language"]]).start()
        # play_music_randomly(context_variables["language"])

    elif context_variables['activity'] == "story":
        Thread(target=stop_program).start()
        Thread(target=play_story_randomly, args=[context_variables["language"]]).start()
        # play_story_randomly(context_variables["language"])


def start_program():
    active = False
    while not active:
        active = activate()
    print("Program has started")
    return True

main()
