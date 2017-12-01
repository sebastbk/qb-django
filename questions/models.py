from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
User = get_user_model()

from common.models import AuditMixin, LikesMixin, TagsMixin


class AnswerMixin(models.Model):
    TEXT = 'text'
    NUMBER = 'number'
    DATE = 'date'
    TIME = 'time'
    ANSWER_WIDGET_CHOICES = (
        (TEXT, 'Text'),
        (NUMBER, 'Number'),
        (DATE, 'Date'),
        (TIME, 'Time'),
    )
    answer = models.CharField(max_length=30)
    alternate_answer = models.CharField(max_length=30, blank=True)
    answer_widget = models.CharField(
        max_length=6,
        choices=ANSWER_WIDGET_CHOICES,
        default=TEXT,
    )

    class Meta:
        abstract = True


class Question(AuditMixin, TagsMixin, LikesMixin, AnswerMixin):
    text = models.TextField(max_length=255)
    difficulty = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return str(self.id)


class Set(AuditMixin, TagsMixin, LikesMixin):
    """A Set of Questions.

    Sets may only contain Questions that share a tag with the set.
    """
    title = models.CharField(
        max_length=30,
        unique=True,
    )
    description = models.TextField(max_length=255)
    questions = models.ManyToManyField(
        Question,
        related_name='sets',
        related_query_name='set',
    )

    def __str__(self):
        return self.title
