from django.urls import path
from userslist.views import UserlistView, UserlistViewDetail

urlpatterns = [
    path("userlist/", UserlistView.as_view()),
    path("userlist/<str:anime_id>/myanimes", UserlistViewDetail.as_view())
]