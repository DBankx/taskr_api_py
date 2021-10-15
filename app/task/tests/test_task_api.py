from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.models import Task
from datetime import datetime
from task import serializers

TASK_URL = reverse('task:task-list')
MY_TASK_URL = reverse('task:task-my-tasks')

def task_detail_url(task_id):
	"""Generate task detail url from provided id"""

	return reverse('task:task-detail', args=[task_id])

def create_sample_task(creator, **extra_fields):

	defaults = {
		'title':'New test task',
		'description':'This is the description of a new task',
		'price':350.00,
		'created_at':datetime.now(),
		'delivery_date':datetime.now(),
	}

	defaults.update(extra_fields)

	return Task.objects.create(creator=creator, **defaults)

class PublicTaskApiTest(TestCase):
	"""Test the task api publicly"""

	def setUp(self):
		self.client = APIClient()


	def test_auth_needed_for_task(self):

		res = self.client.get(TASK_URL)

		self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateTaskApiTest(TestCase):
	"""Private Test Task Api"""

	def setUp(self):
		self.client = APIClient()
		self.user = get_user_model().objects.create(email='test@test.com', password='testpass123', name='test man')
		self.client.force_authenticate(self.user)


	def test_create_task_successful(self):
		"""Test user can create task successfully"""

		pass

	def test_create_task_invalid_details(self):
		"""Test user can create task successfully"""

		pass

	def test_retrieve_tasks_successfully(self):
		"""Test user can retrieve tasks successfully"""

		create_sample_task(creator=self.user)
		create_sample_task(creator=self.user, title='Sample Test 2')

		res = self.client.get(TASK_URL)

		tasks = Task.objects.all().order_by('-created_at')

		serializer = serializers.TaskSerializer(tasks, many=True)

		self.assertEqual(res.status_code, status.HTTP_200_OK)

		self.assertEqual(len(res.data), 2)

		self.assertEqual(res.data, serializer.data)


	def test_retrieve_task_created_by_user(self):
		"""Test that users can retrieve their own tasks"""

		user2 = get_user_model().objects.create_user(email='test2@test.com', password='testpass231', name='test man2', username='defaultszx')

		create_sample_task(creator=user2, title='main user 2 sample task')
		create_sample_task(creator=user2, title='user 2 sample task')

		main_task = create_sample_task(creator=self.user, title='This is the main user task')

		res = self.client.get(MY_TASK_URL)

		self.assertEqual(res.status_code, status.HTTP_200_OK)

		self.assertEqual(len(res.data), 1)

		self.assertEqual(res.data[0]['title'], main_task.title)


	def test_task_partial_update(self):
		"""Test updating task with patch"""

		create_sample_task(creator=self.user)

		new_task = create_sample_task(creator=self.user, title='New task by user')

		payload = {
			'title': 'mad rugged',
			'price': 52.00
		}

		res = self.client.patch(task_detail_url(new_task.id), payload)

		new_task.refresh_from_db()

		self.assertEqual(new_task.price, payload['price'])
