import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import reverse

class Poll(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=200, blank=True)
    open_from = models.DateTimeField(default=timezone.now, blank=True)
    close_at = models.DateTimeField(null=True, blank=True)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s-%s' % (self.user.username, self.title)

    def get_absolute_url(self):
        return reverse('polls:detail', kwargs={'pk': self.pk})

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Open',
    )
    def is_open(self):
        now = timezone.now()
        return self.open_from < now < self.close_at if self.close_at else self.open_from < now


class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    timestamp = models.DateTimeField('vote timestamp', default=timezone.now)
    voter_name = models.CharField(max_length=50)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
