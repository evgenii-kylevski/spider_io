from django.contrib import admin
from scrapper.models import CatalogMobile, MobileProduct


@admin.register(CatalogMobile)
class CatalogMobileAdminPanel(admin.ModelAdmin):
    list_display = ('product_name', 'brand_url', 'product_price')
    list_filter = ('brand_name',)
    search_fields = ('product_name',)
    ordering = ('-product_price',)


@admin.register(MobileProduct)
class MobileProductAdminPanel(admin.ModelAdmin):
    list_display = ('product_name', 'product_description', 'lowprice', 'highprice')
    search_fields = ('product_name',)
    ordering = ('lowprice', 'highprice')
