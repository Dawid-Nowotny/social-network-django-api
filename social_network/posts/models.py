from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    creation_date = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts')