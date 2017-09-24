from django.views.generic import ListView
from .models import Question


class QuestionListView(ListView):
    model = Question
