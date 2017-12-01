from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator


class AuditMixin(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(app_label)s_%(class)ss',
        related_query_name='%(app_label)s_%(class)s',
        editable=False,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class LikesMixin(models.Model):
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='likes_%(app_label)s_%(class)ss',
        related_query_name='likes_%(app_label)s_%(class)s',
    )

    class Meta:
        abstract = True


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


class TagsMixin(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name='%(app_label)s_%(class)ss',
        related_query_name='%(app_label)s_%(class)s',
    )

    class Meta:
        abstract = True
