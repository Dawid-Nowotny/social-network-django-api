from rest_framework import generics, permissions, status
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from .serializers import UserSerializer, AvatarSerializer
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