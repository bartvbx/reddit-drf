from django.urls import path
from .views import PostView, PostDetailView, SubredditView, SubredditDetailView


urlpatterns = [
    path("r/", SubredditView.as_view(), name="subreddit"),
    path("r/<int:pk>/", SubredditDetailView.as_view(), name="subreddit_detail"),
    path("posts/", PostView.as_view(), name="subreddit_posts"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
]
