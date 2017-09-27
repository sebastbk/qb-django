from django import forms

class QuestionFilterForm(forms.Form):
    q = forms.CharField(label='Search', max_length=100)
