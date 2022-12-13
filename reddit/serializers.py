from rest_framework import serializers

from .models import Comment, Post, Subreddit


class SubredditSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Subreddit
        fields = ['id', 'name', 'description', 'owner']


class SubredditDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subreddit
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': False},
            'description': {'required': False},
            'owner': {'required': False},
            'moderator': {'required': False, "allow_null": True}
        }


class SubredditPostsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'text', 'author']
        extra_kwargs = {
            'author': {'required': False},
            'subreddit': {'required': False}
        }


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'subreddit', 'author']
        extra_kwargs = {
            'author': {'required': False},
        }


class PostDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            'title': {'required': False},
            'text': {'required': False},
            'subreddit': {'required': False},
            'author': {'required': False}
        }


class PostCommentsSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'text' : {'required': True},
            'post': {'required': False},
            'author': {'required': False}
        }


class CommentDetailSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'text': {'required': False},
            'post': {'read_only': True},
            'author': {'read_only': True}
        }
