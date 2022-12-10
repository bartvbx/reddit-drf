from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Post, Subreddit
from .serializers import PostDetailSerializer, PostSerializer, SubredditDetailSerializer, SubredditSerializer


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


class PostsTest(APITestCase):
    """
    Test 'posts' API.
    """
    def setUp(self):
        self.url = reverse('posts')
        self.user = User.objects.create_user('username', 'password')
        self.subreddit = Subreddit.objects.create(name='Subreddit', description='Description', owner=self.user)
        self.data = {'title':'Post title test', 'text':'Post text test', 'subreddit':self.subreddit.pk}

    def test_get_posts_list(self):
        """
        Ensure anyone can view all Post objects.
        """
        Post.objects.create(title=self.data['title'], text=self.data['text'], subreddit=self.subreddit)
        Post.objects.create(title=self.data['title'], text=self.data['text'], subreddit=self.subreddit)

        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        response = self.client.get(self.url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 2)
        self.assertEqual(response.data, serializer.data)

    def test_add_post(self):
        """
        Ensure we can create a new Post object and view it.
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.data, format='json')

        post = Post.objects.first()
        serializer = PostSerializer(post)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_add_post_unauthorized(self):
        """
        Ensure we can't create a new Post object without authorization.
        """
        response = self.client.post(self.url, data=self.data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PostDetailsTest(APITestCase):
    """
    Test 'post_detail' API.
    """
    def setUp(self):
        self.user_subreddit_owner = User.objects.create_user('username1', 'password')
        self.user_subreddit_moderator = User.objects.create_user('username2', 'password')
        self.user_post_author = User.objects.create_user('username3', 'password')
        self.user_no_role = User.objects.create_user('username4', 'password')
        self.subreddit_1 = Subreddit.objects.create(name='Subreddit 1', description='Description', owner=self.user_subreddit_owner)
        self.subreddit_1.moderator.add(self.user_subreddit_moderator)
        self.subreddit_2 = Subreddit.objects.create(name='Subreddit 2', description='Description', owner=self.user_subreddit_owner)
        self.post = Post.objects.create(title='Post title test', text='Post text test', subreddit=self.subreddit_1, author=self.user_post_author)
        self.edit_data = {'title':'Post title edit', 'text':'Post text edit', 'subreddit':self.subreddit_2.pk}
        self.url = reverse('post_detail', kwargs={'pk': self.post.pk})

    def test_get_post_details(self):
        """
        Ensure anyone can view Post object details.
        """
        serializer = PostDetailSerializer(self.post)

        response = self.client.get(self.url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_edit_post_details_author(self):
        """
        Ensure that post author can edit Post object details.
        """
        self.client.force_authenticate(self.user_post_author)

        response = self.client.put(self.url, data=self.edit_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.edit_data['title'])
        self.assertEqual(response.data['text'], self.edit_data['text'])
        self.assertEqual(response.data['subreddit'], self.edit_data['subreddit'])

    def test_edit_post_details_subreddit_owner(self):
        """
        Ensure that subreddit owner can edit Post object details.
        """
        self.client.force_authenticate(self.user_subreddit_owner)

        response = self.client.put(self.url, data=self.edit_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.edit_data['title'])
        self.assertEqual(response.data['text'], self.edit_data['text'])
        self.assertEqual(response.data['subreddit'], self.edit_data['subreddit'])

    def test_edit_post_details_moderator(self):
        """
        Ensure that subreddit moderator can edit Post object details.
        """
        self.client.force_authenticate(self.user_subreddit_moderator)

        response = self.client.put(self.url, data=self.edit_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.edit_data['title'])
        self.assertEqual(response.data['text'], self.edit_data['text'])
        self.assertEqual(response.data['subreddit'], self.edit_data['subreddit'])

    def test_edit_post_details_other_user(self):
        """
        Ensure that other users can't edit Post object details.
        """
        self.client.force_authenticate(self.user_no_role)
        response = self.client.put(self.url, data=self.edit_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_post_details_unauthorized(self):
        """
        Ensure we can't edit Post object details without authorization.
        """
        response = self.client.put(self.url, data=self.edit_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_details_author(self):
        """
        Ensure that post author can delete Post object.
        """
        self.client.force_authenticate(self.user_post_author)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_post_details_subreddit_owner(self):
        """
        Ensure that subreddit owner can delete Post object.
        """
        self.client.force_authenticate(self.user_subreddit_owner)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_post_details_moderator(self):
        """
        Ensure that subreddit moderator can delete Post object.
        """
        self.client.force_authenticate(self.user_subreddit_moderator)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_post_details_other_user(self):
        """
        Ensure that other users can't delete Post object.
        """
        self.client.force_authenticate(self.user_no_role)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_details_unauthorized(self):
        """
        Ensure we can't delete Post object details without authorization.
        """
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
