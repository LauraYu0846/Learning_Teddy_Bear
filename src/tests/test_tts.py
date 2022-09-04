import unittest
from tts import text_to_audio
import os
import warnings


class TexttoSpeechTest(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        if os.path.exists('./speech.mp3'):
            os.remove('./speech.mp3')

    def tearDown(self):
        pass

    def test_text_to_speech(self):
        text_to_audio('test', 'english')
        assert os.path.exists('./speech.mp3')
