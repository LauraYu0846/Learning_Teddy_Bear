import pyaudio
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from environment import stt_key, stt_url
from queue import Queue, Full
import os, sys, contextlib
from utilities import speaker

# initialise everything
CHUNK = 1024
BUFF_MAX_SIZE = CHUNK * 10
q = Queue(maxsize=int(round(BUFF_MAX_SIZE / CHUNK)))

# suppresses ALS messages
@contextlib.contextmanager
def ignore_stderr():
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)


def setup_stt():
    authenticator = IAMAuthenticator(stt_key)
    speech_to_text = SpeechToTextV1(
        authenticator=authenticator
    )

    speech_to_text.set_service_url(stt_url)
    return speech_to_text


# define callback for the speech to text service
class MyRecognizeCallback(RecognizeCallback):
    def _init_(self):
        RecognizeCallback._init_(self)
        self.data = {}
        self.inactivity = False

    # def on_transcription(self, transcript):
    #     print("THIS IS THE TRANSCRIPT", transcript)

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

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
    return None, pyaudio.paContinue


def recognize_using_weboscket(language_model, audio_source):
    # initialize speech to text service
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
    with ignore_stderr():
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
    audio_source = AudioSource(q, True, True)
    recognize_using_weboscket(model_dict[language], audio_source)

    while not mycallback.inactivity:
        pass

    # stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    audio_source.completed_recording()

    try:
        text_string = mycallback.data['results'][0]["alternatives"][0]["transcript"]

    except (TypeError, AttributeError):
        text_string = ""
        speaker("Sorry, I have not heard you for one minute. Bye bye. ")
        exit()

    return text_string

# print(transcribe_live_audio("english"))