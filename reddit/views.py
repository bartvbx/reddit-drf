from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Subreddit
from .serializers import SubredditSerializer


class SubredditView(ListCreateAPIView):
    serializer_class = SubredditSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Subreddit.objects.all()


class SubredditDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubredditSerializer
    queryset = Subreddit.objects.all()
