from django.db import models
from django.utils import timezone


class CatalogMobile(models.Model):
    brand_name = models.CharField(max_length=250)
    product_name = models.CharField(max_length=250)
    brand_url = models.URLField(max_length=250)
    product_slug = models.SlugField(max_length=250,
                                    unique_for_date='scrapping_time')
    product_price = models.DecimalField(decimal_places=2, max_digits=100000)
    scrapping_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.product_name


class MobileProduct(models.Model):
    product_name = models.OneToOneField(CatalogMobile,
                                        on_delete=models.CASCADE)
    brand_url = models.URLField(max_length=250)
    product_description = models.TextField()
    lowprice = models.IntegerField()
    highprice = models.IntegerField()
    offercount = models.IntegerField()
    scrapping_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.brand_url
