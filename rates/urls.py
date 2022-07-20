from django.urls import path
from .views import RatesView

urlpatterns = [path("rate/", RatesView.as_view())]
