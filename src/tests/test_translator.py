import unittest
from translator import translate_language


class TranslatorTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_correct_translation(self):
        self.assertEqual(translate_language("hello", "spanish"), "hola")




