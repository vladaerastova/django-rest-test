from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Account
import json

# Create your tests here.


class LoginTest(TestCase):

	def setUp(self):
		self.username = 'user1'
		self.password = 'user1'
		self.email = 'user1@gmail.com'
		self.data = {
			'username': self.username,
			'password': self.password
		}

	def test_login_with_wrong_credentials(self):
		url = reverse('login')
		user = User.objects.create_user(username='user1', email='user1@gmail.com', password='user')
		self.assertEqual(user.is_active, 1, 'Active User')

		response = self.client.post(url, self.data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)

	def test_login_with_right_credentials(self):
		url = reverse('login')
		user = User.objects.create_user(username='user1', email='user1@gmail.com', password='user1')
		self.assertEqual(user.is_active, 1, 'Active User')

		response = self.client.post(url, self.data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
		self.assertEqual('token' in json.loads(response.content).keys(), True)


class RegistrationTest(TestCase):

	def setUp(self):
		self.url = reverse('register')
		self.username = 'user1'
		self.password = 'user1'
		self.email = 'user1@gmail.com'
		self.data = {
			'username': self.username,
			'password': self.password,
			'email': self.email
		}

	def test_registration(self):
		user_count = User.objects.all().count()

		response = self.client.post(self.url, self.data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
		self.assertEqual(User.objects.all().count(), user_count + 1)

	def test_creation_user_account(self):
		response = self.client.post(self.url, self.data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
		user = User.objects.latest('id')
		self.assertEqual(Account.objects.filter(user=user).count(), 1)

	def test_registration_without_email(self):
		user_count = User.objects.all().count()

		response = self.client.post(self.url, {'username': self.username, 'password': self.password}, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
		self.assertEqual(User.objects.all().count(), user_count)

	def test_registration_without_username(self):
		user_count = User.objects.all().count()

		response = self.client.post(self.url, {'email': self.email, 'password': self.password}, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
		self.assertEqual(User.objects.all().count(), user_count)

	def test_registration_without_password(self):
		user_count = User.objects.all().count()

		response = self.client.post(self.url, {'username': self.username, 'email': self.email}, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
		self.assertEqual(User.objects.all().count(), user_count)

	def test_registration_with_nonunique_username(self):
		user_count = User.objects.all().count()

		response = self.client.post(self.url, self.data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
		self.assertEqual(User.objects.all().count(), user_count + 1)

		response = self.client.post(self.url, {'username': self.username, 'email': 'user2@gmail.com', 'password': self.password}, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
		self.assertEqual(json.loads(response.content)['username'][0], u'A user with that username already exists.')
		self.assertEqual(User.objects.all().count(), user_count + 1)

	def test_registration_with_nonunique_email(self):
		user_count = User.objects.all().count()

		response = self.client.post(self.url, self.data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
		self.assertEqual(User.objects.all().count(), user_count + 1)

		response = self.client.post(self.url, {'username': 'user2', 'email': self.email, 'password': self.password}, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
		self.assertEqual(json.loads(response.content)['email'][0], u'This user has already registered.')
		self.assertEqual(User.objects.all().count(), user_count + 1)
