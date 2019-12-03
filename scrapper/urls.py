from django.urls import path
from scrapper.views import *

urlpatterns = [
    path('', scrapper_home, name="home"),
    path('scrapper/', scrapper_app, name="scrapper"),
    path('reports/', reports_list, name="reports"),
    path('scrap-set/', scrapper_set, name="scrap-set"),
]