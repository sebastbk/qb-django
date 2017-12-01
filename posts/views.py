from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework import viewsets

from .serializers import PostSerializer
from .models import Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        user = User.objects.get(pk=1)
        serializer.save(created_by=user)
