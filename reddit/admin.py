from django.contrib import admin

from .models import Comment, Post, Subreddit


admin.site.register(Subreddit)
admin.site.register(Post)
admin.site.register(Comment)
