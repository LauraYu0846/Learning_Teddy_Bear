from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from environment import tts_key, tts_url
import os


# Setup Service
def setup_tts():
    authenticator = IAMAuthenticator(tts_key)
    tts = TextToSpeechV1(authenticator=authenticator)
    tts.set_service_url(tts_url)
    return tts


def text_to_audio(text, language="english"):
    tts = setup_tts()
    voice_dict = {"english": "en-GB_KateV3Voice",
                  "spanish": "es-ES_LauraV3Voice",
                  "french": "fr-FR_ReneeV3Voice"
                  }

    # Convert with a basic language model
    with open('./speech.mp3', 'wb') as audio_file:
        res = tts.synthesize(text, accept='audio/mp3', voice=voice_dict[language]).get_result()
        audio_file.write(res.content)


def play_audio_file():
    #  Try this for raspberry pi
    # apt install mpg123
    os.system("mpg123 -q speech.mp3")
