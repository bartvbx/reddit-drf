from rest_framework import serializers

from .models import Comment, Post, Subreddit


class SubredditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subreddit
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Post
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
