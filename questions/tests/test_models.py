from unittest import mock
from django.test import TestCase

from ..models import Answer
from utils.strings import fuzzy_match, strict_match

class AnswerTestCase(TestCase):
    def test_answer_to_list(self):
        self.assertListEqual(Answer(wordings='puzzle').to_list(), ['puzzle'])
        self.assertListEqual(Answer(wordings='puzzle,riddle').to_list(), ['puzzle', 'riddle'])
        self.assertListEqual(Answer(wordings=' puzzle , riddle ').to_list(), ['puzzle', 'riddle'])
        self.assertListEqual(Answer(wordings=',').to_list(), ['', ''])

    def test_get_matching_func(self):
        self.assertEqual(Answer(matching=Answer.FUZZY).get_matching_func(), fuzzy_match)
        self.assertEqual(Answer(matching=Answer.STRICT).get_matching_func(), strict_match)
        self.assertEqual(Answer(matching='').get_matching_func(), fuzzy_match)
