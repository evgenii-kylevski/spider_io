from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('scrapper/', views.scrap_home, name="scrapper"),
    path('scrap_result/', views.scrap_result, name="scrap_result"),
    path('reports/', views.reports_list, name="reports"),
    path('down_csv', views.down_csv, name="down_csv")
]
