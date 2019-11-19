from django.db import models
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

# Create your models here.

# def scrapper_bot(url):
#     try:
#         html = urlopen(url)
#     except HTTPError as e:
#         return None
#     try:
#         bs

    