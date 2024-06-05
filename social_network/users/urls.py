from django.urls import path

from .views import RegisterView, AvatarView, UserUpdateView, CurrentAvatarView, UserDetailView, AvatarUpdateView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('avatar/', AvatarView.as_view(), name='avatar'),
    path('update/', UserUpdateView.as_view(), name='update'),
    path('avatar/<str:username>/', CurrentAvatarView.as_view(), name='current-avatar'),
    path('users/<str:username>/', UserDetailView.as_view(), name='user-detail'),
    path('avatar/disable/<str:username>/', AvatarUpdateView.as_view(), name='avatar-update'),
]