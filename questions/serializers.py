from rest_framework import serializers
from .models import Question, Answer


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'id',
            'created_by',
            'created_on',
            'text',
            'difficulty',
            'tags',
        )
