from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Comment, Post, Subreddit
from .permissions import (
    IsAuthorOrReadOnly,
    IsOwnerOrReadOnly,
    SubredditOwnerModeratorCommentPermission,
    SubredditOwnerModeratorPostPermission,
    SuperUserPermission
    )
from .serializers import (
    CommentDetailSerializer,
    PostSerializer, PostDetailSerializer, PostCommentsSerializer,
    SubredditSerializer, SubredditDetailSerializer, SubredditPostsSerializer
    )


class SubredditView(ListCreateAPIView):
    serializer_class = SubredditSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Subreddit.objects.all()


class SubredditDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubredditDetailSerializer
    permission_classes = [IsOwnerOrReadOnly|SuperUserPermission]
    queryset = Subreddit.objects.all()


class SubredditPostsView(ListCreateAPIView):
    serializer_class = SubredditPostsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        subreddit_posts = Post.objects.filter(subreddit=self.kwargs['pk'])
        return subreddit_posts
    
    def perform_create(self, serializer):
        subreddit = Subreddit.objects.filter(id=self.kwargs['pk']).first()
        return serializer.save(author=self.request.user, subreddit=subreddit)


class PostView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class PostDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthorOrReadOnly|SubredditOwnerModeratorPostPermission|SuperUserPermission]
    queryset = Post.objects.all()


class PostCommentsView(ListCreateAPIView):
    serializer_class = PostCommentsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_pk = self.kwargs['pk']
        post_comments = Comment.objects.filter(post=post_pk)
        return post_comments

    def perform_create(self, serializer):
        post = Post.objects.filter(id=self.kwargs['pk']).first()
        return serializer.save(author=self.request.user, post=post)


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthorOrReadOnly|SubredditOwnerModeratorCommentPermission|SuperUserPermission]
    queryset = Comment.objects.all()
