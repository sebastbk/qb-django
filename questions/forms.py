from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ['created_by', 'created_on']
        labels = {
            'text': _('Question')
        }
