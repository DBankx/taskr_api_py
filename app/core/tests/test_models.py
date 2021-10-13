from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

class ModelsTest(TestCase):
	"""Test the db models"""

	def setUp(self):
		self.test_email = 'test@test.com'
		self.test_password = 'testpass123'

	def test_create_user_with_email_successful(self):
		"""Test creating user with email is successful"""

		user = get_user_model().objects.create_user(email=self.test_email, password=self.test_password)

		self.assertEqual(user.email, self.test_email)

		self.assertTrue(user.check_password(self.test_password))

	def test_new_user_email_normalized(self):
		"""Test that the user email is normalized"""

		user = get_user_model().objects.create_user(email='test@TEST.com', password=self.test_password)

		self.assertEqual(user.email, self.test_email)


	def test_new_user_invalid_email(self):
		"""Test that invalid email raises value error"""

		with self.assertRaises(ValueError):
			get_user_model().objects.create_user(None, password=self.test_password)
					