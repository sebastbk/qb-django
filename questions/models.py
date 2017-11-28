from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

from common.models import AuditMixin, LikesMixin, TagsMixin

User = get_user_model()


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
    alt_answer = models.CharField(max_length=30, blank=True)
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


class ListBase(AuditMixin, LikesMixin, TagsMixin):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=255)
    questions = models.ManyToManyField(
        Question,
        related_name='%(class)ss',
        related_query_name='%(class)s',
    )

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        unique_together = ('created_by', 'title')


class Collection(ListBase):
    """A Collection of Questions.

    Collections may contain any Questions regardless of tags.
    """
    pass


class Set(ListBase):
    """A Set of Questions.

    Sets may only contain Questions that share a tag with the set.
    """
    pass
