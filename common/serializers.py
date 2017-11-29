from rest_framework import serializers

from .models import Tag


class AuditMixin(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )


class LikesMixin(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()

    def get_likes(self, obj):
        return obj.likes.count()

    def get_like(self, obj):
        return False


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name',)


class TagMixin(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
    )
