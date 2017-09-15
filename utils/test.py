from django.test import TestCase
from .strings import fuzzy_match, strict_match

class FuzzyMatchTestCase(TestCase):
    def test_fuzzy_match(self):
        self.assertTrue(fuzzy_match('puzzle', 'puzzle'))
        self.assertTrue(fuzzy_match('puzzle', 'puzzles'))
        self.assertTrue(fuzzy_match('puzzle', 'puzle'))
        self.assertFalse(fuzzy_match('puzzle', 'puzl'))
        self.assertFalse(fuzzy_match('puzzle', 'people'))
        self.assertFalse(fuzzy_match('puzzle', ''))

    def test_strict_match(self):
        self.assertTrue(strict_match('puzzle', 'puzzle'))
        self.assertFalse(strict_match('puzzle', 'puzzles'))
        self.assertFalse(strict_match('puzzle', 'puzle'))
        self.assertFalse(strict_match('puzzle', 'puzl'))
        self.assertFalse(strict_match('puzzle', 'people'))
        self.assertFalse(strict_match('puzzle', ''))
