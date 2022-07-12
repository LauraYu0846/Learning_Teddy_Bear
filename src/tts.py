from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from environment import tts_key, tts_url


# Setup Service
def setup_tts():
    authenticator = IAMAuthenticator(tts_key)
    tts = TextToSpeechV1(authenticator=authenticator)
    tts.set_service_url(tts_url)
    return tts

# Covert with a basic language model
# with open('./speech.mp3', 'wb') as audio_file:
#     res = tts.synthesize('Hello World!', accept='audio/mp3', voice='en-US_AllisonV3Voice').get_result()
#     audio_file.write(res.content)

# # Reading from a file
# with open('churchill.txt', 'r') as f:
#     text = f.readlines()
#
# text = [line.replace('\n','') for line in text]
#
# text = ''.join(str(line) for line in text)
#
# with open('./winston.mp3', 'wb') as audio_file:
#     res = tts.synthesize(text, accept='audio/mp3', voice='en-GB_JamesV3Voice').get_result()
#     audio_file.write(res.content)


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



# text_to_audio()

def play_audio_file():
    # write  code to make it play audio file

    #  Try this for your raspberry pi
    # apt install mpg123
    import os
    os.system("mpg123 speech.mp3")


# # define text string
# phrase = "Good morning"
# language = "spanish"
# text = f"{phrase}. In {language}, this is"
#
# # create audio file and play it
# text_to_audio(text)
# play_audio_file()
#
# spanish_text = "buenos dias"
# text_to_audio(spanish_text, "spanish")
# play_audio_file()

play_audio_file()



