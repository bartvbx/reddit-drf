from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Subreddit
from .serializers import SubredditSerializer


class SubredditView(ListCreateAPIView):
    serializer_class = SubredditSerializer
    queryset = Subreddit.objects.all()


class SubredditDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubredditSerializer
    queryset = Subreddit.objects.all()
