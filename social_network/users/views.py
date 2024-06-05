from rest_framework import generics, permissions, status
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.http import HttpResponse

from .serializers import UserSerializer, AvatarSerializer, ProfileInfoSerializer
from .models import Avatar

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

class AvatarUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None

    def put(self, request, *args, **kwargs):
        user = request.user
        avatars = Avatar.objects.filter(user=user)
        avatars.update(current=False)
        return Response({"detail": "All avatars set to current=False"}, status=status.HTTP_200_OK)

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileInfoSerializer
    lookup_field = 'username'

class CurrentAvatarView(generics.RetrieveAPIView):
    def get_object(self):
        username = self.kwargs.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        avatar = Avatar.objects.filter(user=user, current=True).first()
        if avatar:
            return avatar
        else:
            return Response({'error': 'User has no current avatar'}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if isinstance(instance, HttpResponse):
            return instance
        elif instance and instance.image:
            image_data = instance.image.read()
            return HttpResponse(image_data, content_type='image/jpeg')