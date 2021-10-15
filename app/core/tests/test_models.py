from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from datetime import datetime

def sample_user(email='test@email.com', password='testpass123', name='test man'):
	"""Creates a test sample user"""

	return get_user_model().objects.create_user(email=email, password=password, name=name)

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


	def test_task_str(self):
		"""Test string representation of a task returns the title"""

		task = models.Task.objects.create(
			title='New test task',
			description='This is the description of a new task',
			price=350.00,
			creator=sample_user(),
			created_at=datetime.now(),
			delivery_date=datetime.now(),
		)

		self.assertEqual(str(task), task.title)		
					