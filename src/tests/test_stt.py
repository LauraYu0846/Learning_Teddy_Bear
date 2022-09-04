import unittest
import warnings
from stt import activate, transcribe_live_audio, setup_stt
from threading import Thread
from tts import play_audio_file
import time

class SttTest(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)

    def tearDown(self):
        pass


    def test_stt_setup(self):
        self.assertIsNotNone(setup_stt())

    # def test_activate(self):
    #     # Thread(target=activate).start()
    #     # time.sleep(1)
    #     Thread(target=play_audio_file, args=["tests/audio_files/activate.mp3"]).start()
