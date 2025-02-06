import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import admin


class User(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    mail = models.CharField(max_length=50)

class Announcment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=400)
    title = models.CharField(max_length=50)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return f"Announcement: {self.title}\nContent: {self.description}"

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class UserLog(models.Model):
    actions = [
        ('login', "Login Successfully"),
        ('announcment', "Look announcment list"),
        ('detail', 'View single question info')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_time = models.DateTimeField()
    action = models.CharField(choices=actions, max_length=20)
