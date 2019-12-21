from django.contrib import admin
from scrapper.models import CatalogMobile, MobileProduct


@admin.register(CatalogMobile)
class CatalogMobileAdminPanel(admin.ModelAdmin):
    list_display = ('brand_name', 'brand_url')
    list_filter = ('brand_name',)
    search_fields = ('brand_name',)
    ordering = ('-brand_name',)

@admin.register(MobileProduct)
class MobileProductAdminPanel(admin.ModelAdmin):
    list_display = ('brand_name', 'product_name', 'product_price', 'scrapping_time')
    list_filter = ('brand_name',)
    search_fields = ('product_name',)
    ordering = ('-scrapping_time',)