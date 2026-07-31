from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model to access the application
    """

    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(unique=True)
    profile_pic_url = models.URLField(max_length=500, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email or self.username