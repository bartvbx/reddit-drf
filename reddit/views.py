from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Comment, Post, Subreddit
from .serializers import CommentSerializer, PostSerializer, SubredditSerializer


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


class PostCommentsView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_pk = self.kwargs["pk"]
        post_comments = Comment.objects.filter(post=post_pk)
        return post_comments


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
