from django.urls import path

from .views import PostView, PostViewDetail

app_name = 'posts'

urlpatterns = [
    path('create-post/', PostView.as_view(), name='create-post'),
    path('post/<int:pk>/', PostViewDetail.as_view(), name='post-detail'),
]