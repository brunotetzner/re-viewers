from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser

from users.managers import UserManager


class User(AbstractUser):
    username = None
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=200)
    avatar = models.TextField(null=True)
    
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    
    objects = UserManager()
    
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS = [ "first_name", "last_name", "password" ]
