from django.db import models
from django.contrib.auth.models import User

from posts.models import Post

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    creation_date = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_comments')