from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUserModel(AbstractUser):
    phone_number = models.CharField(max_length=5, blank=True)
    address = models.CharField(max_length=10, blank=True)
    photo = models.ImageField(default='/img/user-profile.png')
