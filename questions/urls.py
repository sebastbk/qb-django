from django.conf.urls import url

from .views import QuestionListView, QuestionCreateView


urlpatterns = [
    url(r'^$', QuestionListView.as_view(), name='list'),
    url(r'^create/$', QuestionCreateView.as_view(), name='create'),
]
