from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Subreddit
from .serializers import SubredditDetailSerializer, SubredditSerializer


class SubredditsTest(APITestCase):
    """
    Test 'subreddits' API.
    """
    def setUp(self):
        self.url = reverse('subreddits')
        self.user = User.objects.create_user('username', 'password')
        self.client.force_authenticate(self.user)
        self.data = {'name':'Subreddit test', 'description':'Description test'}
        
    def test_get_subreddits_list(self):
        """
        Ensure we can view all Subreddit objects.
        """
        Subreddit.objects.create(name='Subreddit 1', description='Description 1')
        Subreddit.objects.create(name='Subreddit 2', description='Description 2')

        subreddits = Subreddit.objects.all()
        serializer = SubredditSerializer(subreddits, many=True)

        response = self.client.get(self.url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 2)
        self.assertEqual(response.data, serializer.data)

    def test_add_subreddit(self):
        """
        Ensure we can create a new Subreddit object and view it.
        """
        response = self.client.post(self.url, data=self.data, format='json')

        subreddit = Subreddit.objects.first()
        serializer = SubredditSerializer(subreddit)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_add_subreddit_unauthorized(self):
        """
        Ensure we can't create a new Subreddit object without authorization.
        """
        self.client.force_authenticate(user=None)
        
        response = self.client.post(self.url, data=self.data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SubredditDetailsTest(APITestCase):
    """
    Test 'subreddit_detail' API.
    """
    def setUp(self):
        self.user1 = User.objects.create_user('username1', 'password')
        self.user2 = User.objects.create_user('username2', 'password')
        self.subreddit = Subreddit.objects.create(name='Subreddit', description='Description', owner=self.user1)
        self.edit_data = {'name':'Subreddit edited', 'description':'Description edited', 'owner':self.user2.pk}
        self.url = reverse('subreddit_detail', kwargs={'pk': self.subreddit.pk})

    def test_get_subreddit_details(self):
        """
        Ensure we can view Subreddit object details.
        """
        serializer = SubredditDetailSerializer(self.subreddit)

        response = self.client.get(self.url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_edit_subreddit_details_owner(self):
        """
        Ensure that subreddit owner can edit Subreddit object details.
        """
        self.client.force_authenticate(self.user1)

        response = self.client.put(self.url, data=self.edit_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.edit_data['name'])
        self.assertEqual(response.data['description'], self.edit_data['description'])
        self.assertEqual(response.data['owner'], self.edit_data['owner'])

    def test_edit_subreddit_details_other_user(self):
        """
        Ensure that other users can't edit Subreddit object details.
        """
        self.client.force_authenticate(self.user2)
        response = self.client.put(self.url, data=self.edit_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_subreddit_details_unauthorized(self):
        """
        Ensure we can't edit Subreddit object details without authorization.
        """
        response = self.client.put(self.url, data=self.edit_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_subreddit_details_owner(self):
        """
        Ensure that subreddit owner can delete Subreddit object.
        """
        self.client.force_authenticate(self.user1)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_subreddit_details_other_user(self):
        """
        Ensure that other users can't delete Subreddit object.
        """
        self.client.force_authenticate(self.user2)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_subreddit_details_unauthorized(self):
        """
        Ensure we can't delete Subreddit object details without authorization.
        """
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
