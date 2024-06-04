from rest_framework import generics, permissions

from django.contrib.auth.models import User

from .serializers import UserSerializer, AvatarSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class AvatarView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AvatarSerializer