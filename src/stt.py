import contextlib
import os
import sys
import pyaudio
import speech_recognition as sr
import subprocess
from queue import Queue, Full
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from environment import stt_key, stt_url


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
        self.main_program_active = False

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

    def on_hypothesis(self, hypothesis):
        if "teddy" in hypothesis:
            print(hypothesis)
            print("I heard Teddy")
            self.main_program_active = True
            print(self.main_program_active)
            print("\n")


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


# this function will initiate the recognize service and pass in the AudioSource
def recognize_using_weboscket(language_model, audio_source, timeout=3):
    # initialize speech to text service
    speech_to_text = setup_stt()

    response = speech_to_text.recognize_using_websocket(audio=audio_source,
                                                        content_type='audio/l16; rate=44100',
                                                        recognize_callback=mycallback,
                                                        interim_results=True,
                                                        background_audio_suppression=0.5,
                                                        inactivity_timeout=timeout,
                                                        model=language_model
                                                        )
    return response


def transcribe_live_audio(language="english", timeout=2):
    model_dict = {"english": "en-GB_BroadbandModel",
                  "spanish": "es-ES_BroadbandModel",
                  "french": "fr-FR_BroadbandModel",
                  "japanese": "ja-JP_BroadbandModel",
                  "korea": "ko-KR_BroadbandModel",
                  "chinese": "zh-CN_BroadbandModel",
                  "german": "de-DE_BroadbandModel",
                  "italian": "it-IT_BroadbandModel",
                  "Portuguese": "pt-BR_BroadbandModel",
                  "Dutch": "nl-NL_BroadbandModel"
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
    recognize_using_weboscket(model_dict[language], audio_source, timeout)

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
        text_string = "No"
#         speaker("Sorry, I have not heard anything. Goodbye. ")
#         exit()

    if "stop" in text_string:
        os._exit(0)

    return text_string


def activate():
    command = take_command()
    if 'teddy' in command:
        return True
    else:
        return False


def stop():
    command = take_command()
    if 'stop' in command:
        subprocess.call(['killall', 'mpg123'])
        print("TRIED TO STOP PROGRAM")
        os._exit(0)
    else:
        return False


def stop_program():
    stopped = False
    while not stopped:
        stopped = stop()


def take_command():
    with ignore_stderr():
        r = sr.Recognizer()
        m = sr.Microphone()

        try:
            with m as source: r.adjust_for_ambient_noise(source)
            with m as source: audio = r.listen(source)
            try:
                # recognize speech using Google Speech Recognition
                value = r.recognize_google(audio)
                print("You said {}".format(value))
                return value.lower()
            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
                return ""
            except sr.RequestError as e:
                print("Couldn't request results from Google Speech Recognition service; {0}".format(e))
                return ""
        except:
            return ""
