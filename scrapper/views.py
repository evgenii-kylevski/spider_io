from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def scrapper_base(request):
    return render(request, 'scrapper/base.html')