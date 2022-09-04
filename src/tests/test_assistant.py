import unittest
import warnings
from assistant import send_stateless_message, new_session, message, get_context_variables_from_response


class AssistantTest(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        self.session_id = new_session()

    def tearDown(self):
        pass

    def test_stateless_message(self):
        msg = send_stateless_message("hello")
        expected = "I didn't get your meaning. Could you repeat it again?"
        self.assertEqual(expected, msg)

    def test_create_new_session(self):
        self.assertIsNotNone(new_session())

    def test_message(self):
        expected = (
            'Hello. I am Teddy Bear. What do you want to do today, learn a new language, listen to music, or read a story?',
            False)
        self.assertEqual(message(self.session_id, ""), expected)

    def test_get_context_variables_from_response(self):
        context_variables = {'activity': "music", 'language': 'spanish'}
        response = {
            "context": {"skills": {
                "main skill": {
                    "user_defined": context_variables
                }
            }}
        }
        self.assertEqual(context_variables, get_context_variables_from_response(response))
