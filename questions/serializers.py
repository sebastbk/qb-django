from rest_framework import serializers
from .models import Question, Answer, Tag


class ManyToManyListField(serializers.ListField):
    def __init__(self, *args, **kwargs):
        self.field = kwargs.pop('field', None)
        assert self.field is not None, (
            "The field argument must be set to a field of the related model."
        )
        super().__init__(*args, **kwargs)

    def to_representation(self, data):
        data = data.values_list(self.field, flat=True)
        return super().to_representation(data)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text', 'alt1', 'alt2', 'type',)
        read_only_fields = ('question',)


class QuestionSerializer(serializers.ModelSerializer):
    tags = ManyToManyListField(
        field='name',
        child=serializers.CharField(min_length=3, max_length=30)
    )
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'created_by', 'created_on', 'text', 'difficulty', 'tags', 'answers')

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        answers_data = validated_data.pop('answers')
        question = Question.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_data)
            question.tags.add(tag)
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)
        return question

    def update_tags(self, instance, tags_data):
        instance_tags = instance.tags.all()
        tags = [
            Tag.objects.get_or_create(name=tag_data)[0]
            for tag_data in tags_data
        ]
        # add new tags
        for tag in tags:
            if tag not in instance_tags:
                instance.tags.add(tag)
        # remove discarded tags
        for instance_tag in instance_tags:
            if instance_tag not in tags:
                instance.tags.remove(instance_tag)

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        answers_data = validated_data.pop('answers', None)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        if tags_data is not None:
            self.update_tags(instance, tags_data)
        return instance
