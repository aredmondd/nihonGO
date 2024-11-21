from django.contrib.auth.models import User
from django.db import models

class Friend(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_of', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} is friends with {self.friend.username}" if self.is_accepted else f"{self.user.username} sent a friend request to {self.friend.username}"

class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='chatrooms')

    def __str__(self):
        return self.name

class PrivateChat(models.Model):
    user1 = models.ForeignKey(User, related_name='chats_as_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='chats_as_user2', on_delete=models.CASCADE)

    def __str__(self):
        return f"Chat between {self.user1.username} and {self.user2.username}"
