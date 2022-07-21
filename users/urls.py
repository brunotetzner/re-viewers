from django.urls import path

from users.views import (
    UserRegisterView,
    UserLoginView,
    UserView,
    AdminView,
    AdminIdView,
)


urlpatterns = [
    path("users/register/", UserRegisterView.as_view()),
    path("users/login/", UserLoginView.as_view()),
    path("users/profile/", UserView.as_view()),
    path("users/", AdminView.as_view()),
    path("users/<str:id>/", AdminIdView.as_view()),
]
