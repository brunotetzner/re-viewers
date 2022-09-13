from django.db import models
from uuid import uuid4
from django.core.validators import MinValueValidator, MaxValueValidator


class AnimeStatus(models.TextChoices):
    PRODUCTION = "On going"
    CANCELED = "Canceled"
    FINISHED = "Finished"


class Anime(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    image = models.CharField(max_length=128)
    title = models.CharField(unique=True, max_length=50)
    sinopse = models.CharField(max_length=2000)
    studio = models.CharField(max_length=30)
    banner = models.CharField(max_length=128)
    original_title = models.CharField(unique=True, max_length=50)
    launch_data = models.DateField()
    average_rate = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], default=0
    )
    users = models.ManyToManyField("users.User", through="animes.Rate")
    status = models.CharField(
        max_length=30,
        choices=AnimeStatus.choices,
    )
    categories = models.ManyToManyField("categories.Category")
    comments = models.ManyToManyField(
        "users.User", through="animes.Comment", related_name="Anime_comments"
    )


class Rate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    anime = models.ForeignKey("animes.Anime", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    anime = models.ForeignKey("animes.Anime", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    comment = models.CharField(max_length=144)
