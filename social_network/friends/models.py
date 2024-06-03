from django.db import models
from django.contrib.auth.models import User

class FriendshipStatus(models.IntegerChoices):
    PENDING = 1, 'Pending'
    ACCEPTED = 2, 'Accepted'
    REJECTED = 3, 'Rejected'

class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_initiated')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_received')
    status = models.IntegerField(choices=FriendshipStatus.choices, default=FriendshipStatus.PENDING)
    creation_date = models.DateField(auto_now_add=True)
