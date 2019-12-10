import datetime
from django.db import models
from django.utils import timezone


# class Domain(models.Model):
#     url_domain = models.CharField(max_length=250)
#     title = models.CharField(max_length=250)
#     name_domain = models.CharField(max_length=250)

# class PageSite(models.Model):
#     url_page = models.URLField(max_length=250)
#     title = models.CharField(max_length=250)
#     slug = models.SlugField(max_length=250)
#     h1 = models.CharField(max_length=250)
#     description = models.TextField()
#     created_ad = models.DateTimeField(auto_now_add=True)
#
# class Session(models.Model):
#     user = models.CharField(max_length=250)
#     name_domain = models.ForeignKey(Domain,
#                                     on_delete=models.CASCADE)
#     date_session = models.CharField(max_length=250)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class PageSite(models.Model):
    h1 = models.CharField(max_length=250)
