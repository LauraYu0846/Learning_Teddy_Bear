from tts import text_to_audio, play_audio_file
from stt import transcribe_live_audio
from translator import translate_language

# define text string
phrase = transcribe_live_audio(language="english")

output_language = "spanish"
text = f"{phrase} in {output_language} is"

# create audio file and play i
text_to_audio(text)
play_audio_file()

spanish_text = translate_language(phrase, "spanish")
text_to_audio(spanish_text, "spanish")
play_audio_file()
