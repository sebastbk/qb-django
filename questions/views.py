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
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from common.models import Tag
from common.serializers import TagSerializer
from common.permissions import IsCreatorOrReadOnly

from .models import Question, Set
from .serializers import QuestionSerializer, SetSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )
    filter_backends = (
        filters.SearchFilter,
    )
    search_fields = ('name',)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (
        IsCreatorOrReadOnly,
    )
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    filter_fields = (
        'created_by',
        'difficulty',
    )
    search_fields = ('=tags__name',)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


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
    permission_classes = (
        IsCreatorOrReadOnly,
    )

    def perform_create(self, serializer):
        user = User.objects.get(pk=1)
        serializer.save(created_by=user)
