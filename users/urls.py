from django.urls import path

from users.views import UserRegisterView


urlpatterns = [
    path("users/register/", UserRegisterView.as_view()),
]
