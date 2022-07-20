from django.urls import path
from .views import ListAndCreateAnimesView

urlpatterns = [
    path('animes/', ListAndCreateAnimesView.as_view()),
  
]