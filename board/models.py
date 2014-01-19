from django.contrib.auth.models import User
from django.db import models

class Board(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique = True)
    open_for = models.ForeignKey(User, related_name = "user")
    admin = models.ForeignKey(User, related_name = "admin")
    opening = models.DateTimeField(blank = True, null = True)
    closing = models.DateTimeField(blank = True, null = True)

    def get_absolute_url(self):
        url = '/board/' + self.slug
        return url

class Comment(models.Model):
    text = models.TextField()
    belongs_to = models.ForeignKey(Board, related_name="messages")
    post_date = models.DateTimeField()
    votes = models.IntegerField(default=0)
