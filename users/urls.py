from django.urls import path

from users.views import UserRegisterView, LoginView


urlpatterns = [
    path("users/register/", UserRegisterView.as_view()),
    path("users/login/", LoginView.as_view()),
]
