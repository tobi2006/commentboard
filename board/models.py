from django.contrib.auth.models import User
from django.db import models

class Board(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique = True)
    open_for = models.ManyToManyField(User, related_name = "user")
    admins = models.ManyToManyField(User, related_name = "admin")
    opening = models.DateTimeField()
    closing = models.DateTimeField()

class Message(models.Model):
    text = models.TextField()
    belongs_to = models.ForeignKey(Board, related_name="messages")
    post_date = models.DateTimeField()
    votes = models.IntegerField(default=0)
