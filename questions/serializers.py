from rest_framework import serializers

from .validators.serializers import is_true
from .models import Tag, Question, Answer, Set


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class InlineAnswerSerializer(serializers.ModelSerializer):
    delete = serializers.BooleanField(
        write_only=True,
        required=False,
        validators=[is_true]
    )

    class Meta:
        model = Answer
        fields = ('id', 'text', 'alt1', 'alt2', 'type', 'delete')
        read_only_fields = ('question',)
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},
        }

    def validate(self, data):
        """Check that an id field is included if the delete field is given."""
        if 'delete' in data and 'id' not in data:
            raise serializers.ValidationError(
                "The id field must be provided with the delete field.")
        return data


class QuestionSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    answers = InlineAnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'created_by',
            'created_on',
            'last_modified_on',
            'text',
            'difficulty',
            'tags',
            'answers'
        )

    def create_answers(self, instance, answers_data):
        for answer_data in answers_data:
            Answer.objects.create(question=instance, **answer_data)

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        question = Question.objects.create(**validated_data)
        self.create_answers(question, answers_data)
        return question

    def update_answers(self, instance, answers_data):
        instance_answers = instance.answers.all()
        new_data = [a for a in answers_data if 'id' not in a]
        updated_data = [a for a in answers_data if 'id' in a]
        deleted_ids = [a['id'] for a in updated_data if a.get('delete', False)]
        # remove deleted answers
        instance_answers.filter(id__in=deleted_ids).delete()
        # update existing answers
        for answer_data in updated_data:
            id = answer_data.pop('id')
            if id not in deleted_ids:
                instance_answers.filter(id=id).update(**answer_data)
        # add new answers
        self.create_answers(instance, new_data)

    def update(self, instance, validated_data):
        answers_data = validated_data.pop('answers')
        self.update_answers(instance, answers_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class SetSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    
    class Meta:
        model = Set
        fields = (
            'id',
            'created_by',
            'created_on',
            'last_modified_on',
            'title',
        )