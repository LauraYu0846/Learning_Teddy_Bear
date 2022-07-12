import pyaudio
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from threading import Thread
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from environment import stt_key, stt_url
from queue import Queue, Full

# initialise everything
CHUNK = 1024
BUFF_MAX_SIZE = CHUNK * 10
q = Queue(maxsize=int(round(BUFF_MAX_SIZE / CHUNK)))

audio_source = AudioSource(q, True, True)


def setup_stt():
    authenticator = IAMAuthenticator(stt_key)
    speech_to_text = SpeechToTextV1(
        authenticator=authenticator
    )

    speech_to_text.set_service_url(stt_url)
    return speech_to_text


# define callback for the speech to text service
class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)
        self.data = ""
        self.inactivity = False

    # def on_transcription(self, transcript):
    #     print("THIS IS THE TRANSCRIPT", transcript)

    def on_connected(self):
        print('Connection was successful')

    # def on_error(self, error):
    #     print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))
        self.inactivity = True

    def on_listening(self):
        print('Service is listening')

    # def on_hypothesis(self, hypothesis):
    #     print(hypothesis)

    def on_data(self, data):
        # print(data)
        self.data = data

    def on_close(self):
        print("Connection closed")


mycallback = MyRecognizeCallback()


def pyaudio_callback(in_data, frame_count, time_info, status):
    try:
        q.put(in_data)
    except Full:
        pass  # discard
    return (None, pyaudio.paContinue)


def recognize_using_weboscket(*args):
    # initialize speech to text service
    language_model = args[0]
    speech_to_text = setup_stt()

    response = speech_to_text.recognize_using_websocket(audio=audio_source,
                                                        content_type='audio/l16; rate=44100',
                                                        recognize_callback=mycallback,
                                                        interim_results=True,
                                                        background_audio_suppression=0.5,
                                                        inactivity_timeout=2,
                                                        model=language_model
                                                        )

    return response


def transcribe_live_audio(language="english"):
    model_dict = {"english": "en-GB_BroadbandModel",
                  "spanish": "es-ES_BroadbandModel",
                  "french": "fr-FR_BroadbandModel"
                  }
    # instantiate pyaudio
    audio = pyaudio.PyAudio()

    # open stream using callback
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=CHUNK,
        stream_callback=pyaudio_callback,
        start=False
    )

    stream.start_stream()

    recognize_thread = Thread(target=recognize_using_weboscket, args=(model_dict[language],))
    recognize_thread.start()

    while not mycallback.inactivity:
        pass

    # stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    audio_source.completed_recording()

    text_string = ""
    try:
        text_string = mycallback.data['results'][0]["alternatives"][0]["transcript"]

    except TypeError:
        text_string = ""

    return text_string
