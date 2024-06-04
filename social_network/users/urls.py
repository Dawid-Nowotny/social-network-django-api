from django.urls import path

from .views import RegisterView, AvatarView, UserUpdateView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('avatar/', AvatarView.as_view(), name='avatar'),
    path('update/', UserUpdateView.as_view(), name='update'),
]