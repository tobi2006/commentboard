from django.contrib.auth.models import User
from django.db import models

class board(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    open_for = models.ManyToManyField(User, related_name = "user")
    admins = models.ManyToManyField(User, related_name = "admin")
    opening = models.DateTimeField()
    closing = models.DateTimeField()

class message(models.Model):
    message = models.TextField()
    post_date = models.DateTimeField()
    votes = models.IntegerField(default=0)
