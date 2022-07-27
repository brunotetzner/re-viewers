from django.urls import path
from .views import AnimeView, AnimeIdView, AnimeByCategory

urlpatterns = [
    path("animes/", AnimeView.as_view()),
    path("animes/category/", AnimeByCategory.as_view()),
    path("animes/<id>/", AnimeIdView.as_view()),
]
