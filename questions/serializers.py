from rest_framework import serializers

from .models import Tag, Question, Set


class TagMixin(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
    )


class AuditMixin(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name',)


class QuestionSerializer(AuditMixin, TagMixin, serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'id',
            'created_by',
            'created_on',
            'modified_on',
            'difficulty',
            'text',
            'answer',
            'alternate_answer',
            'answer_type',
            'tags',
        )


class SetSerializer(AuditMixin, TagMixin, serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = (
            'id',
            'created_by',
            'created_on',
            'modified_on',
            'title',
            'tags',
        )
