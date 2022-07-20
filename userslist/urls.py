from django.urls import path
from userslist.views import UserlistView, UserlistViewDetail

urlpatterns = [
    path("userlist/", UserlistView.as_view()),
    path("userlist/<int:anime_id>/", UserlistViewDetail.as_view())
]