import unicodedata
from difflib import SequenceMatcher as Matcher


def strip_non_alphanumerics(s):
    """Strips any characters that are not a-z A-Z 0-9."""
    return ''.join(c for c in s if c.isalnum())


def strip_accents(s):
    """Replaces accented characters with non accented ones."""
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def normalize(s):
    """Removes all punctuation, whitespace, and accents. Converts to lowercase."""
    return strip_accents(strip_non_alphanumerics(s)).lower()


def fuzzy_match(s1, s2, threshold=0.9):
    ratio = Matcher(None, normalize(s1), normalize(s2)).ratio()
    return ratio >= threshold


def strict_match(s1, s2):
    return strip_accents(s1.strip().lower()) == strip_accents(s2.strip().lower())
