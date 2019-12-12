from django.db import models
from django.utils import timezone

class PubManager(models.Manager):
    def get_query_set(self):
        return super(PubManager, self).get_queryset('scrapping_time')


class Session(models.Model):
    h1 = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    url = models.URLField(max_length=250)
    scrapping_time = models.DateTimeField(default=timezone.now)
    object = models.Manager()
    pubs = PubManager()

    def __str__(self):
        return self.h1
