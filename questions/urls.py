from django.conf.urls import url

from .views import QuestionListCreateView, QuestionRetrieveUpdateDestoryView


urlpatterns = [
    url(r'^$', QuestionListCreateView.as_view()),
    url(r'^(?P<pk>\d+)$', QuestionRetrieveUpdateDestoryView.as_view()),
]
