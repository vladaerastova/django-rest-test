from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from .models import Like
from posts.models import Post
from .api.serializers import LikeSerializer
import json

# Create your tests here.


class LikeListTest(TestCase):

	def setUp(self):
		self.client = APIClient()
		user = User.objects.create_user(username='user1', email='user1@gmail.com', password='user1')
		response = self.client.post(reverse('login'), {'username': 'user1', 'password': 'user1'}, format='json')
		self.token = json.loads(response.content).get('token')
		self.post1 = Post.objects.create(title='post1', slug='post1', content='content', user=user)
		self.url = reverse('list_like')

	def test_unauthorized_get_all_likes(self):
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.content)

	def test_authorized_get_all_likes(self):
		self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(self.token))
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)


class GetSingleLikeTest(TestCase):

	def setUp(self):
		user = User.objects.create_user(username='user1', email='user1@gmail.com', password='user1')
		response = self.client.post(reverse('login'), {'username': 'user1', 'password': 'user1'}, format='json')
		self.token = json.loads(response.content).get('token')
		self.post1 = Post.objects.create(title='post1', slug='post1', content='content', user=user)
		self.like = Like.objects.create(user=user, post=self.post1)

	def test_get_valid_single_like(self):
		url = reverse('detail_like', kwargs={'pk': self.like.pk})
		response = self.client.get(url)
		like = Like.objects.get(pk=self.like.pk)
		serializer = LikeSerializer(like, context={'request': Request(APIRequestFactory().get('/'))})
		self.assertEqual(response.data['result'], serializer.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

	def test_get_invalid_single_like(self):
		url = reverse('detail_like', kwargs={'pk': 30})
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)


class CreateNewLikeTest(TestCase):

	def setUp(self):
		self.client = APIClient()
		self.user = User.objects.create_user(username='user1', email='user1@gmail.com', password='user1')
		self.post1 = Post.objects.create(title='post1', slug='post1', content='content', user=self.user)
		response = self.client.post(reverse('login'), {'username': 'user1', 'password': 'user1'}, format='json')
		self.token = json.loads(response.content).get('token')
		self.url = reverse('create_like')

	def test_unauthorized_create_like(self):
		response = self.client.post(
			self.url,
			data=json.dumps({'post': self.post1.pk}),
			content_type='application/json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.content)

	def test_create_valid_like(self):
		self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(self.token))
		response = self.client.post(
			self.url,
			data=json.dumps({'post': self.post1.pk}),
			content_type='application/json'
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_create_invalid_like(self):
		self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(self.token))
		response = self.client.post(
			self.url,
			data=json.dumps({'post': 30}),
			content_type='application/json'
		)
		self.assertEqual(json.loads(response.content)['non_field_errors'][0], u'Incorrect post id')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_invalid_double_like(self):
		self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(self.token))
		self.like = Like.objects.create(user=self.user, post=self.post1)
		response = self.client.post(
			self.url,
			data=json.dumps({'post': self.post1.pk}),
			content_type='application/json'
		)
		self.assertEqual(json.loads(response.content)['non_field_errors'][0], u'Like already exists')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleLikeTest(TestCase):

	def setUp(self):
		self.client = APIClient()
		user = User.objects.create_user(username='user1', email='user1@gmail.com', password='user1')
		response = self.client.post(reverse('login'), {'username': 'user1', 'password': 'user1'}, format='json')
		self.token = json.loads(response.content).get('token')
		self.post1 = Post.objects.create(title='post1', slug='post1', content='content', user=user)
		self.like = Like.objects.create(user=user, post=self.post1)

	def test_valid_delete_like(self):
		url = reverse('detail_like', kwargs={'pk': self.like.pk})
		self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(self.token))
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_invalid_delete_like(self):
		url = reverse('detail_like', kwargs={'pk': 30})
		self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(self.token))
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_not_owner_delete_single_like(self):
		url = reverse('detail_like', kwargs={'pk': self.like.pk})
		User.objects.create_user(username='user2', email='user2@gmail.com', password='user2')
		response = self.client.post(reverse('login'), {'username': 'user2', 'password': 'user2'}, format='json')
		self.token = json.loads(response.content).get('token')
		self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(self.token))
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
