from django.contrib import admin
from scrapper.models import PageSite, Question, Choice

admin.site.register(PageSite)
admin.site.register(Question)
admin.site.register(Choice)