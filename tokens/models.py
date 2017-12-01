import uuid

from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


def create_key():
    return uuid.uuid4().hex


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(is_active=True)


class Token(models.Model):
    user = models.ForeignKey(
        User,
        related_name='tokens',
        related_query_name='token',
    )
    key = models.CharField(
        max_length=100,
        primary_key=True,
        default=create_key,
    )
    is_active = models.BooleanField(default=False)

    objects = ActiveManager()

    def __str__(self):
        return ' '.join(('Token', str(self.key)))

    def save(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError
