from rest_framework import serializers

from common.serializers import AuditMixin, LikesMixin, TagMixin
from .models import Question, Set


class QuestionSerializer(AuditMixin, LikesMixin, TagMixin, serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'id',
            'created_by',
            'created_on',
            'modified_on',
            'likes',
            'like',
            'tags',
            'difficulty',
            'text',
            'answer',
            'alternate_answer',
            'answer_widget',
        )


class SetSerializer(AuditMixin, LikesMixin, TagMixin, serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = (
            'id',
            'created_by',
            'created_on',
            'modified_on',
            'likes',
            'like',
            'tags',
            'title',
            'description',
        )
