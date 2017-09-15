from django.db import models
from django.contrib.auth import get_user_model
from .validators import validate_comma_separated_string_list
from utils.strings import fuzzy_match, strict_match
User = get_user_model()


class Difficulty(models.Model):
    name = models.CharField(max_length=30, unique=True)
    rank = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['rank']
        verbose_name_plural = 'Difficulties'


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'


class Question(models.Model):
    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category)
    difficulty = models.ForeignKey(Difficulty)
    text = models.TextField(max_length=255)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-created_on']


class Answer(models.Model):
    FUZZY = 'FU'
    STRICT = 'ST'
    MATCHING_CHOICES = (
        (FUZZY, 'Fuzzy'),
        (STRICT, 'Strict'),
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    wordings = models.CharField(max_length=255, validators=[validate_comma_separated_string_list],
                                help_text='If the answer can be written in several ways use a comma '
                                          'separated list of wordings.')
    matching = models.CharField(max_length=2, choices=MATCHING_CHOICES, default=FUZZY, 
                                help_text='The comparison method for checking if an answer is correct.\n'
                                          '- Fuzzy matching attempts to compensate for spelling.\n'
                                          '- Strict matching will only compensate for symbols, whitespace, '
                                          'casing, and accents.')

    def get_matching_func(self):
        """Returns a comparison function based on the matching field."""
        return fuzzy_match if self.matching == FUZZY else strict_match

    def check_answer(self, answer):
        """Compares a string to the answer for correctness."""
        matching_func = self.get_matching_func()
        return any(matching_func(w, answer) for w in self.to_list())

    def to_list(self):
        """Returns a list of wordings."""
        return (x.strip() for x in self.wordings.split(','))

    def __str__(self):
        return ' or '.join(self.to_list())

    class Meta:
        order_with_respect_to = 'question'
