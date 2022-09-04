import unittest
from translator import translate_language
import warnings


class TranslatorTest(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)

    def tearDown(self):
        pass

    def test_correct_translation(self):
        self.assertEqual(translate_language("hello", "spanish"), "hola")




