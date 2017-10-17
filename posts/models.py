from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    created_by = models.ForeignKey(
        User,
        editable=False
    )
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified_on = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=30)
    text = models.TextField(max_length=255)
