from django.db import models

from common.models import AuditMixin


class Post(AuditMixin):
    title = models.CharField(max_length=30)
    lead = models.TextField(max_length=255)
    body = models.TextField(max_length=1023)
    image = models.ImageField()
