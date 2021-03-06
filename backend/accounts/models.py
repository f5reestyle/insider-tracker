from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    telegram_id = models.CharField(null=True,max_length=12)
    email = models.EmailField()
    api_key = models.CharField(max_length=50, null=True)

