from rest_framework import generics, permissions

from .serializers import PostSerializer

class PostView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]