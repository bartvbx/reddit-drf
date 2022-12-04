from django.urls import path
from .views import SubredditView, SubredditDetailView


urlpatterns = [
    path("r/", SubredditView.as_view(), name="subreddit"),
    path("r/<int:pk>/", SubredditDetailView.as_view(), name="subreddit_detail"),
]
