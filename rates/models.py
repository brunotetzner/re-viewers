# from django.db import models
# from uuid import uuid4
# from django.core.validators import MinValueValidator, MaxValueValidator


# class Rate(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     anime = models.ForeignKey("animes.Anime", on_delete=models.CASCADE)
#     user = models.ForeignKey("users.User", on_delete=models.CASCADE)
#     rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])