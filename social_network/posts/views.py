from rest_framework import generics, permissions

from .models import Post
from .serializers import PostSerializer, PostDetailSerializer

class PostView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostViewDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer