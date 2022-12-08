from django.urls import path
from .views import PostCommentsView, CommentDetailView, PostView, PostDetailView, SubredditView, SubredditDetailView, SubredditPostsView


urlpatterns = [
    path('subreddits/', SubredditView.as_view(), name='subreddits'),
    path('subreddits/<int:pk>/', SubredditDetailView.as_view(), name='subreddit_detail'),
    path('subreddits/<int:pk>/posts/', SubredditPostsView.as_view(), name='subreddit_posts'),
    path('posts/', PostView.as_view(), name='posts'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/comments/', PostCommentsView.as_view(), name='post_comments'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment_detail'),
]
