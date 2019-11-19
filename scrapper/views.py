from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def scrapper_home(request):
    return render(request, 'scrapper/home.html')

def scrapper_app(request):
    return render(request, 'scrapper/scrapper_app.html')

def reports_list(request):
    return render(request, 'scrapper/reports.html')

def scrapper_set(request):
    return render(request, 'scrapper/scrap_set.html')