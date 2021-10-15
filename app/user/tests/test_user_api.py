from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

# Generate the user url
CREATE_USER_URL = reverse('user:register')
LOGIN_USER_URL = reverse('user:login')
PROFILE_URL = reverse('user:profile')

class PublicUserApiTest(TestCase):
	"""Test the public user api"""

	def setUp(self):
		self.client = APIClient()

	def test_user_register_with_success(self):
		"""Test the registration of user with email and password is successful"""

		payload = {
			'email': 'test@test.com',
			'name': 'test man',
			'password': 'testpass123'
		}

		res = self.client.post(CREATE_USER_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_201_CREATED)

		user = get_user_model().objects.get(**res.data)

		self.assertTrue(user.check_password(payload['password']))

		self.assertNotIn('password', res.data)


	def test_user_already_exists(self):
		"""Test that user already exists"""

		payload = {
			'email': 'test@test.com',
			'password': 'testpass123',
			'name': 'test man'
		}

		get_user_model().objects.create_user(**payload)

		res = self.client.post(CREATE_USER_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


	def test_user_login_successful(self):
		"""Test that user logs in successfully"""

		payload = {
			'email': 'test@test.com',
			'password': 'testpass123',
			'name': 'test man'
		}	

		get_user_model().objects.create_user(**payload)

		res = self.client.post(LOGIN_USER_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_200_OK)

		self.assertIn('token', res.data)

	def test_user_login_invalid_credentials(self):
		"""Test that token is not created if invalid credentials are provided"""

		payload = {
			'email': 'test@test.com',
			'password': 'testpass123',
		}	

		get_user_model().objects.create_user(**payload)

		res = self.client.post(LOGIN_USER_URL, {'email': 'test@test.com', 'password': 'pa$$w0rd'})

		self.assertNotIn('token', res.data)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserApiTest(TestCase):
	"""Test the private user apis"""

	def setUp(self):
		self.client = APIClient()
		self.user = get_user_model().objects.create_user(
			email='test@test.com',
			password='testpass123'
		)
		self.client.force_authenticate(self.user)

	def test_retrieve_profile_success(self):
		"""Test that user can see their profiles"""

		res = self.client.get(PROFILE_URL)

		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data['email'], self.user.email)

	def test_update_profile_successful(self):
		"""Test that user can update their profile using patch"""

		payload = {
			'country': 'Nigeria',
			'bio': 'im a good guy'
		}

		res = self.client.patch(PROFILE_URL, payload)

		self.user.refresh_from_db()

		self.assertEqual(self.user.country, payload['country'])
		
		self.assertEqual(res.status_code, status.HTTP_200_OK)


