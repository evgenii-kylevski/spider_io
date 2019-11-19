from django.urls import path
from scrapper.views import *

urlpatterns = [
    path('', scrapper_home),
    path('scrapper', scrapper_app),
    path('reports', reports_list),
    path('scrap-set', scrapper_set),
]