from datetime import datetime
from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from utils.strings import fuzzy_match, strict_match
User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=30,
        validators=[MinLengthValidator(3)],
        unique=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Question(models.Model):
    created_by = models.ForeignKey(
        User,
        editable=False
    )
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified_on = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=255)
    difficulty = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    tags = models.ManyToManyField(
        Tag, 
        related_name='questions',
        related_query_name="question",
    )

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.text


class CharTypeMixin(object):
    """Helper class for storing several stringable datatypes into a charfield."""
    TEXT = 'str'
    NUMBER = 'int'
    DATE = 'date'
    TIME = 'time'
    TYPE_CHOICES = (
        (TEXT, 'Text'),
        (NUMBER, 'Number'),
        (DATE, 'Date'),
        (TIME, 'Time'),
    )

    EXTRACT_FUNCTIONS = {
        TEXT: str,
        NUMBER: int,
        DATE: lambda x: datetime.strptime(x, '%Y-%m-%d').date(),
        TIME: lambda x: datetime.strptime(x, '%H:%M:%S').time(),
    }

    @classmethod
    def get_extract_func(cls, extract_type):
        if extract_type not in cls.EXTRACT_FUNCTIONS:
            raise ValueError('Invalid extract type: %(extract_type)s.' % {'extract_type': extract_type})
        return cls.EXTRACT_FUNCTIONS[extract_type]

    PACKING_FUNCTIONS = {
        TEXT: str,
        NUMBER: str,
        DATE: lambda x: x.strftime('%Y-%m-%d'),
        TIME: lambda x: x.strftime('%H:%M:%S'),
    }

    @classmethod
    def get_packing_func(cls, packing_type):
        if packing_type not in cls.PACKING_FUNCTIONS:
            raise ValueError('Invalid extract type: %(packing_type)s.' % {'packing_type': packing_type})
        return cls.PACKING_FUNCTIONS[packing_type]


class MatchingMixin(object):
    FUZZY = 'FU'
    STRICT = 'ST'
    MATCHING_CHOICES = (
        (FUZZY, 'Fuzzy'),
        (STRICT, 'Strict'),
    )
    MATCHING_FUNCTIONS = {
        FUZZY: fuzzy_match,
        STRICT: strict_match,
    }

    def get_matching_func(matching_type):
        if matching_type not in MATCHING_FUNCTIONS:
            raise ValueError('Invalid matching type: %(matching_type)s.' % {'matching_type': matching_type})
        return MATCHING_FUNCTIONS[matching_type]



class Answer(models.Model):
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE,
        related_name='answers',
        related_query_name='answer',
    )
    text = models.CharField(max_length=30)
    alt1 = models.CharField(max_length=30, blank=True)
    alt2 = models.CharField(max_length=30, blank=True)
    type = models.CharField(
        max_length=4,
        choices=CharTypeMixin.TYPE_CHOICES,
        default=CharTypeMixin.TEXT, 
        help_text='The format of the answer.'
    )

    class Meta:
        order_with_respect_to = 'question'
    
    def __str__(self):
        return ' or '.join(self.list())

    def list(self):
        return filter(None, [self.text, self.alt1, self.alt2])


class Set(models.Model):
    created_by = models.ForeignKey(
        User,
        editable=False
    )
    created_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(
        max_length=30, 
        validators=[MinLengthValidator(3)],
        unique=True
    )
    questions = models.ManyToManyField(
        Question,
        related_name='sets',
        related_query_name='set'
    )


class RatingBase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        editable=False
    )
    value = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.value)


class QuestionRating(RatingBase):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='ratings',
        related_query_name='rating'
    )

    class Meta:
        unique_together = ('question', 'user')


class SetRating(RatingBase):
    set = models.ForeignKey(
        Set,
        on_delete=models.CASCADE,
        related_name='ratings',
        related_query_name='rating'
    )

    class Meta:
        unique_together = ('set', 'user')
