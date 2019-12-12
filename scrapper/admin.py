from django.contrib import admin
from scrapper.models import Session


@admin.register(Session)
class SessionAdminPanel(admin.ModelAdmin):
    list_display = ('url', 'h1', 'scrapping_time')
    list_filter = ('url',)
    search_fields = ('h1',)
    ordering = ('-scrapping_time',)
