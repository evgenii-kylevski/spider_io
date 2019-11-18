from django.urls import path
from scrapper.views import scrapper_base

urlpatterns = [
    path('', scrapper_base)
]