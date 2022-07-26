from tts import text_to_audio, play_audio_file
from stt import transcribe_live_audio
from assistant import new_session, message, get_context_variables
from translator import translate_language
import utilities


session_id = new_session()


def watson_conversation():
    for i in range(4):
        if i == 0:
            user_message = ""
        else:
            user_message = transcribe_live_audio(language="english")

        watson_response = message(session_id, user_message)
        utilities.speaker(watson_response)

    return get_context_variables(session_id)

print(watson_conversation())

# # Greeting part
# # Flow 1 - Asking name
# watson_response = message(session_id, "")
#
# utilities.speaker(watson_response)
#
# user_message = transcribe_live_audio(language="english")
#
# # Flow 2 - Asking language
# watson_response = message(session_id, user_message)
#
# utilities.speaker(watson_response)
#
# user_message = transcribe_live_audio(language="english")
#
# # Flow 3 - Asking difficulty
# watson_response = message(session_id, user_message)
#
# utilities.speaker(watson_response)
#
# user_message = transcribe_live_audio(language="english")
#
# # Confirming variables
# watson_response = message(session_id, user_message)
#
# utilities.speaker(watson_response)
#
# # print(get_context_variables(session_id))
#
# #
# # # with open
# # with open('questions.json') as questionbank:
# #     q = json.load(questionbank)
# #     print(q)
# #
#
#
# # # define text string
# phrase = transcribe_live_audio(language="english")
#
# output_language = "spanish"
# text = f"{phrase} in {output_language} is"
#
# # create audio file and play i
# text_to_audio(text)
# play_audio_file()
#
# spanish_text = translate_language(phrase, "spanish")
# text_to_audio(spanish_text, "spanish")
# play_audio_file()
# #
#
# # json file to contain all the questions (just created at pycharm)
