from functools import reduce

from django.db.models import Q
from django.shortcuts import reverse, get_object_or_404
from django.views.generic.list import ListView
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework import viewsets, filters
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from common.models import Tag
from common.serializers import TagSerializer

from .models import Question, Set
from .serializers import QuestionSerializer, SetSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    filter_fields = (
        'created_by__username',
        'difficulty',
    )
    search_fields = ('=tags__name',)

    def perform_create(self, serializer):
        user = User.objects.get(pk=1)
        serializer.save(created_by=user)


class SetQuestions:
    @detail_route(url_path='questions')
    def questions(self, request, pk=None):
        questions = self.get_object().questions.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
        

    @detail_route(
        methods=['post'],
        url_path='questions/add',
        url_name='questions-add',
    )
    def questions_add(self, request, pk=None):
        id_list = request.data.get('questions', [])
        questions = Question.objects.filter(id__in=id_list)
        self.get_object().questions.add(*questions)
        content = {
            'status': 'success'
        }
        return Response(content)

    @detail_route(
        methods=['post', 'delete'],
        url_path='questions/remove',
        url_name='questions-remove',
    )
    def questions_remove(self, request, pk=None):
        id_list = request.data.get('questions', [])
        questions = Question.objects.filter(id__in=id_list)
        self.get_object().questions.remove(*questions)
        content = {
            'status': 'success'
        }
        return Response(content)


class SetViewSet(viewsets.ModelViewSet, SetQuestions):
    queryset = Set.objects.all()
    serializer_class = SetSerializer

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
