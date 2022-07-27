from django.urls import path
from .views import (
    AnimeView,
    AnimeIdView,
    RetrieveAnimeView,
    AnimeByCategory,
    GetByRateView
)

urlpatterns = [
    path("animes/", AnimeView.as_view()),
    path("animes/category/", AnimeByCategory.as_view()),
    path("animes/one/<str:pk>/", RetrieveAnimeView.as_view()),
    path("animes/<id>/", AnimeIdView.as_view()),
    path("animes/best/<int:anime_amount>/", GetByRateView.as_view()),
]
