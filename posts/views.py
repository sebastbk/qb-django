from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework import viewsets

from common.permissions import IsStaffOrReadOnly

from .serializers import PostSerializer
from .models import Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsStaffOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
