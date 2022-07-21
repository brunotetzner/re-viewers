from django.urls import path
from .views import RatesView, RatesIdView

urlpatterns = [path("rate/", RatesView.as_view()), path("rate/<str:anime_id>/", RatesIdView.as_view())]
