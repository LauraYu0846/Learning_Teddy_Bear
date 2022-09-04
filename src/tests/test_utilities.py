import unittest
import warnings
import json
from utilities import get_num_questions, random_question


class AssistantTest(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)

    def tearDown(self):
        pass

    def test_get_num_questions(self):
        self.assertGreaterEqual((get_num_questions("one")), 2)

    def test_random_question(self):
        with open('questions.json') as questionbank:
            question_dict = json.load(questionbank)
            question = random_question(question_dict, "one")[0]
            assert question not in question_dict['one'].values()

