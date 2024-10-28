from django.db import models
from django.contrib.auth.models import User

#-Profile class
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='nihonGO\nihonGO\theme\media\default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

