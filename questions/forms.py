from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from .models import Question, Answer


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        exclude = ['created_by', 'created_on']
        labels = {
            'text': _('Question')
        }


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['answer', 'alt1', 'alt2', 'data_type']


AnswersFormSet = inlineformset_factory(
    Question, Answer, form=AnswerForm, extra=2)
