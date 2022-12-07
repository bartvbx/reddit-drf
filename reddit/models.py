from django.contrib.auth.models import User
from django.db import models


class Subreddit(models.Model):
    name = models.CharField(max_length=256, unique=True, blank=False, null=False)
    description = models.TextField(max_length=512, blank=True, null=True)
    owner = models.ForeignKey(User, related_name='owns_subreddit', on_delete=models.SET_NULL, blank=False, null=True)
    moderator = models.ManyToManyField(User, related_name='moderates_subreddit')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=256, blank=False, null=False)
    text = models.TextField(max_length=512, blank=True, null=True)
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(max_length=512, blank=False, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text
