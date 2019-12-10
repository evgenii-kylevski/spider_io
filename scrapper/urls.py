from django.urls import path
# from scrapper.views import *
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('scrapper/', views.scrap_home, name="scrapper"),
    path('scrap_result/', views.scrap_result, name="scrap_result"),
    path('reports/', views.reports_list, name="reports"),
    path('scrap-set/', views.scrapper_set, name="scrap-set"),
]

# urlpatterns += [
#     path('polls/', views.index, name='index'),
#     path('polls/<int:question_id>/', views.detail, name='detail'),
#     path('polls/<int:question_id>/results/', views.results, name='results'),
#     path('polls/<int:question_id>/vote/', views.vote, name='vote'),
# ]

urlpatterns += [
    path('polls/', views.IndexView.as_view(), name='index'),
    path('polls/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('polls/<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('polls/<int:question_id>/vote/', views.vote, name='vote'),
]