from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Post, Subreddit
from .serializers import PostSerializer, SubredditSerializer


class SubredditView(ListCreateAPIView):
    serializer_class = SubredditSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Subreddit.objects.all()


class SubredditDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubredditSerializer
    queryset = Subreddit.objects.all()


class PostView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()


class PostDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
