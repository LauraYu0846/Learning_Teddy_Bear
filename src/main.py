from tts import text_to_audio, play_audio_file
from stt import transcribe_live_audio
from assistant import new_session, message
from translator import translate_language

# assistant
session_id = new_session()
conversation = message(session_id, "")
text_to_audio(conversation)
play_audio_file()

user_message = transcribe_live_audio(language="english")
conversation = message(session_id, user_message)

text_to_audio(conversation)
play_audio_file()

# # define text string
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


# json file to contain all the questions (just created at pycharm)
