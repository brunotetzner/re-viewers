from django.db import models
from uuid import uuid4
from django.core.validators import MinValueValidator, MaxValueValidator

    


class Anime(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    image = models.CharField(max_length=128)
    title = models.CharField(max_length=50)
    sinopse = models.CharField(max_length=512)
    studio = models.CharField(max_length=30)
    banner = models.CharField(max_length=128)
    original_title = models.CharField(max_length=50)
    launch_data = models.DateField()
    users = models.ManyToManyField("users.User", through="animes.Rate")
    status = models.CharField(max_length=15, default="not started")
    categories = models.ManyToManyField("categories.Category")
    

class Rate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    anime = models.ForeignKey("animes.Anime", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])