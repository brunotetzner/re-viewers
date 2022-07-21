from django.urls import path
from .views import AnimeView

urlpatterns = [
    path("animes/", AnimeView.as_view()),
]
