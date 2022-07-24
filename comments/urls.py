from django.urls import path
from .views import CommentView, CommentAnimeIdView, CommentIdView

urlpatterns = [
    path("comments/", CommentView.as_view()),
    path("comments/anime/<str:anime_id>/", CommentAnimeIdView.as_view()),
    path("comments/<str:comment_id>/", CommentIdView.as_view()),
]
