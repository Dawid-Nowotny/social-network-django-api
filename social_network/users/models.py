from django.db import models
from django.contrib.auth.models import User

class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='avatars')
    image = models.ImageField(upload_to='images/avatars')
    current = models.BooleanField(default=True)