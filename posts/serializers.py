from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    
    class Meta:
        model = Post
        fields = ('id', 'created_by', 'created_on', 'last_modified_on', 'title', 'text')
