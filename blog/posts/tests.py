from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from .models import Post
from .api.serializers import PostSerializer
import json

# Create your tests here.


class PostListTest(TestCase):

	def setUp(self):
		self.client = APIClient()
		user = User.objects.create_user(username='user1', email='user1@gmail.com', password='user1')
		response = self.client.post(reverse('login'), {'username': 'user1', 'password': 'user1'}, format='json')
		self.token = json.loads(response.content).get('token')
		Post.objects.create(title='post1', slug='post1', content='content', user=user)
		Post.objects.create(title='post2', slug='post2', content='content', user=user)
		Post.objects.create(title='post3', slug='post3', content='content', user=user)
		self.url = reverse('list')

	def test_unauthorized_get_all_posts(self):
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.content)

	def test_authorized_get_all_posts(self):
		self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(self.token))
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)


class GetSinglePostTest(TestCase):

	def setUp(self):
		user = User.objects.create_user(username='user1', email='user1@gmail.com', password='user1')
		response = self.client.post(reverse('login'), {'username': 'user1', 'password': 'user1'}, format='json')
		self.token = json.loads(response.content).get('token')
		self.post1 = Post.objects.create(title='post1', slug='post1', content='content', user=user)
		self.post2 = Post.objects.create(title='post2', slug='post2', content='content', user=user)

	def test_get_valid_single_post(self):
		url = reverse('detail', kwargs={'slug': self.post1.slug})
		response = self.client.get(url)
		post = Post.objects.get(pk=self.post1.pk)
		serializer = PostSerializer(post, context={'request': Request(APIRequestFactory().get('/'))})
		self.assertEqual(response.data['result'], serializer.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

	def test_get_invalid_single_post(self):
		url = reverse('detail', kwargs={'slug': 'post5'})
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)


class CreateNewPostTest(TestCase):

	def setUp(self):
		self.client = APIClient()
		user = User.objects.create_user(username='user1', email='user1@gmail.com', password='user1')
		response = self.client.post(reverse('login'), {'username': 'user1', 'password': 'user1'}, format='json')
		self.token = json.loads(response.content).get('token')
		self.url = reverse('create_post')
		self.valid_payload = {
			'title': 'Post1',
			'content': 'content'
		}
		self.invalid_payload = {
			'title': '',
			'content': 'content'
		}

	def test_unauthorized_create_post(self):
		response = self.client.post(
			self.url,
			data=json.dumps(self.valid_payload),
			content_type='application/json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.content)

	def test_create_valid_post(self):
		self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(self.token))
		response = self.client.post(
			self.url,
			data=json.dumps(self.valid_payload),
			content_type='application/json'
		)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_create_invalid_post(self):
		self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(self.token))
		response = self.client.post(
			self.url,
			data=json.dumps(self.invalid_payload),
			content_type='application/json'
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSinglePostTest(TestCase):

	def setUp(self):
		self.client = APIClient()
		user = User.objects.create_user(username='user1', email='user1@gmail.com', password='user1')
		response = self.client.post(reverse('login'), {'username': 'user1', 'password': 'user1'}, format='json')
		self.token = json.loads(response.content).get('token')
		self.post1 = Post.objects.create(title='post1', slug='post1', content='content', user=user)
		self.post2 = Post.objects.create(title='post2', slug='post2', content='content', user=user)
		self.url = reverse('detail', kwargs={'slug': self.post1.slug})
		self.valid_payload = {
			'title': 'Post1',
			'content': 'content'
		}
		self.invalid_payload = {
			'title': '',
			'content': 'content'
		}

	def test_valid_update_post(self):
		self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(self.token))
		response = self.client.patch(
			self.url,
			data=json.dumps(self.valid_payload),
			content_type='application/json'
		)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_invalid_update_post(self):
		self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(self.token))
		response = self.client.patch(
			self.url,
			data=json.dumps(self.invalid_payload),
			content_type='application/json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_not_owner_update_single_post(self):
		User.objects.create_user(username='user2', email='user2@gmail.com', password='user2')
		response = self.client.post(reverse('login'), {'username': 'user2', 'password': 'user2'}, format='json')
		self.token = json.loads(response.content).get('token')
		self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(self.token))
		response = self.client.patch(
			self.url,
			data=json.dumps(self.valid_payload),
			content_type='application/json'
		)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DeleteSinglePostTest(TestCase):

	def setUp(self):
		self.client = APIClient()
		user = User.objects.create_user(username='user1', email='user1@gmail.com', password='user1')
		response = self.client.post(reverse('login'), {'username': 'user1', 'password': 'user1'}, format='json')
		self.token = json.loads(response.content).get('token')
		self.post1 = Post.objects.create(title='post1', slug='post1', content='content', user=user)
		self.post2 = Post.objects.create(title='post2', slug='post2', content='content', user=user)

	def test_valid_delete_post(self):
		url = reverse('detail', kwargs={'slug': self.post1.slug})
		self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(self.token))
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_invalid_delete_post(self):
		url = reverse('detail', kwargs={'slug': 'post6'})
		self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(self.token))
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_not_owner_delete_single_post(self):
		url = reverse('detail', kwargs={'slug': self.post2.slug})
		User.objects.create_user(username='user2', email='user2@gmail.com', password='user2')
		response = self.client.post(reverse('login'), {'username': 'user2', 'password': 'user2'}, format='json')
		self.token = json.loads(response.content).get('token')
		self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(self.token))
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
