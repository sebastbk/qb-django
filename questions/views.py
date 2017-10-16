from functools import reduce
from django.db.models import Q
from django.shortcuts import reverse
from django.views.generic.list import ListView
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import viewsets
from .models import Question
from .serializers import QuestionSerializer
User = get_user_model()


COMMON_WORDS = set(['to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'up', 'about', 'into', 'over', 'after', 'the', 'and', 'a', 'that', 'i', 'it', 'not', 'he', 'as', 'you', 'this', 'but', 'his', 'they', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their'])


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        user = User.objects.get(pk=1)
        serializer.save(created_by=user)


class SearchView(ListView):
    search_fields = None

    def get_search_terms(self):
        search_query = self.request.GET.get('search_query', '')
        return [x.replace('_', ' ') for x in search_query.split() if x not in COMMON_WORDS] or None

    def get_queryset(self):
        if self.search_fields is None:
            raise ImproperlyConfigured(
                "No search fields provided. Please provide search fields.")
        queryset = super().get_queryset()
        search_terms = self.get_search_terms()
        if search_terms is not None:
            query_params = ('%(field_name)s__contains' % {'field_name': field} for field in self.search_fields)
            return queryset.filter(reduce(lambda x, y: x | y, 
                [Q(**{param: term}) for param in query_params for term in search_terms]))
        return queryset


class RawQueryMixin(object):
    """Mixin for retrieving the raw query string and returning it as a dictionary."""
    def get_raw_query_string(self):
        return self.request.META.get('QUERY_STRING', '')

    def get_raw_query_dict(self):
        raw_qs = self.get_raw_query_string()
        params = filter(None, raw_qs.split('&'))  # filter empty param list
        return {k: v for k, v in map(lambda x: x.split('='), params)}


class QuestionListView(RawQueryMixin, SearchView):
    model = Question
    template_name = 'questions/index.html'
    search_fields = ['category__name', 'text']

    def get_filter_difficulty(self):
        try:
            return int(self.request.GET.get('filter'))
        except ValueError:
            return None

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_difficulty = self.get_filter_difficulty()
        if filter_difficulty is not None:
            queryset = queryset.filter(difficulty=filter_difficulty)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'difficulties': Difficulty.objects.all(),
            'filter_difficulty': self.get_filter_difficulty(),
            'search_query': self.get_raw_query_dict().get('search_query', ''),
        })
        return context
