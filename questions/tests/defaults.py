"""Functions to get or create default models objects."""
from django.contrib.auth import get_user_model
from ..models import Difficulty, Category, Question, Answer
User = get_user_model()


def user():
    return User.objects.get_or_create(username='test_admin')[0]


def difficulty():
    return Difficulty.objects.get_or_create(name='test_difficulty', rank=1)[0]


def category():
    return Category.objects.get_or_create(name='test_category')[0]


def question():
    return Question.objects.get_or_create(text='What is a sample question?', 
        defaults={
            'created_by': user(),
            'difficulty': difficulty(),
            'category': category(),
        })[0]
