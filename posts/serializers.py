from rest_framework import serializers

from common.serializers import AuditMixin

from .models import Post


class PostSerializer(AuditMixin, serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'created_by',
            'created_on',
            'modified_on',
            'title',
            'lead',
            'body',
            'image',
        )
