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
    
    animes = models.ManyToManyField("animes.Anime", through="Userlist")
    
    objects = UserManager()
    
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS = [ "first_name", "last_name", "password" ]

 
class ChoicesStatus(models.TextChoices):

    WATCH_LATER = ("Assistir mais tarde")
    WATCHING = ("Assistindo")
    FINISHED = ("Terminado")

class Userlist(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    anime = models.ForeignKey("animes.Anime", related_name="anime", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", related_name="user", on_delete=models.CASCADE)
    watching_status = models.CharField(max_length=50, choices=ChoicesStatus.choices)