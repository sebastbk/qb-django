import uuid
from django.db import models

class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=30, unique=True, null=False, blank=False,
                            help_text='Tags must consist of letters, numbers, and underscores.')

    def __str__(self):
        return self.text
