from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

import zipfile

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
        username = self.kwargs.get('username')

        if user.username != username:
            raise PermissionDenied("You do not have permission to update avatars for this user.")

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
            raise NotFound({'error': 'User not found'})

        avatar = Avatar.objects.filter(user=user, current=True).first()
        if avatar:
            return avatar
        else:
            raise NotFound({'error': 'User has no current avatar'})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if isinstance(instance, HttpResponse):
            return instance
        elif instance and instance.image:
            image_data = instance.image.read()
            return HttpResponse(image_data, content_type='image/jpeg')
        
class UserAvatarsZipView(generics.GenericAPIView):
    lookup_field = 'username'

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        avatars = Avatar.objects.filter(user=user)

        if not avatars:
            return Response({"error": "User has no avatars."}, status=status.HTTP_404_NOT_FOUND)

        zip_filename = "avatars.zip"
        zip_file = zipfile.ZipFile(zip_filename, mode='w')

        try:
            current_avatar = avatars.filter(current=True).first()
            for avatar in avatars:
                avatar_file = default_storage.open(avatar.image.name, 'rb')
                if avatar == current_avatar:
                    file_name = f"current_{avatar.id}.png"
                else:
                    file_name = f"{avatar.id}.png"
                zip_file.writestr(file_name, avatar_file.read())
                avatar_file.close()

            zip_file.close()

            zip_data = open(zip_filename, 'rb').read()
            response = HttpResponse(zip_data, content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
            return response
        finally:
            default_storage.delete(zip_filename)