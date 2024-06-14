from django.urls import path

from .views import PostView

app_name = 'posts'

urlpatterns = [
    path('create-post/', PostView.as_view(), name='create-post'),
]