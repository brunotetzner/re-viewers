from django.urls import path
from .views import RatesView, RatesIdView

urlpatterns = [path("rate/<str:anime_id>/", RatesView.as_view())]
