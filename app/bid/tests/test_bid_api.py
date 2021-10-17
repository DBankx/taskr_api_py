from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.models import Task, Bid
from datetime import datetime
from rest_framework import status
from bid.serializers import BidSerializer

def create_bids_url(task_id):
	"""create bids url from task id"""
	return reverse('bid:list-create', args=[task_id])

def create_manage_bid_url(bid_id, action):
	"""create manage url for bids"""
	return reverse(f'bid:bid-{action}', args=[bid_id])	

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

def create_sample_bid(user, task, **extra_fields):
	"""Create a sample bid for a task"""

	defaults = {
		'description': 'This is a test bid',
		'user': user,
		'task': task,
		'price': 100.00
	}

	defaults.update(extra_fields)

	return Bid.objects.create(**defaults)


class PrivateBidApiTest(TestCase):
	"""test private bid api"""

	def setUp(self):
		self.client = APIClient()
		self.user = get_user_model().objects.create_user(email='test@test.com', password='testpass123', name='test man', username='testman')
		self.client.force_authenticate(self.user)


	def	test_list_bid_for_task_successful(self):
		"""Test list bids return 200"""

		task = create_sample_task(creator=self.user)

		bid = create_sample_bid(user=get_user_model().objects.create_user(email='test2@test.com', password='test2pass123', name='test2 man', username='test2man'), task=task)

		res = self.client.get(create_bids_url(task.id))

		self.assertEqual(res.status_code, status.HTTP_200_OK)

		self.assertEqual(len(res.data), 1)

		self.assertEqual(res.data[0]['task'], task.id)


	def test_create_bid_successful(self):
		"""Test that creating bid is successful"""

		task = create_sample_task(creator=get_user_model().objects.create_user(email='test2@test.com', password='test2pass123', name='test2 man', username='test2man'))

		payload = {
			'price': 520.00,
			'description': 'please let me fix your task',
	
		}	

		res = self.client.post(create_bids_url(task.id), payload)

		self.assertEqual(res.status_code, status.HTTP_201_CREATED)

		self.assertEqual(res.data['task'], task.id)

		self.assertTrue(Bid.objects.filter(id=res.data['id'], task=res.data['task'], user=self.user).exists())


	# def test_task_user_cannot_create_bid(self):
	# 	"""Test that the creator of the task cannot create a bid"""

	# 	task = create_sample_task(creator=self.user)

	# 	payload = {
	# 		'price': 520.00,
	# 		'description': 'please let me fix your task',
	# 	}	

	# 	res = self.client.post(create_bids_url(task.id), payload)

	# 	self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


	def test_retrieve_bid_by_id(self):
		"""Test retrieve bid by id is successful"""

		task = create_sample_task(creator=self.user)

		bid = create_sample_bid(user=get_user_model().objects.create_user(email='test2@test.com', password='test2pass123', name='test2 man', username='test2man'), task=task)

		res = self.client.get(create_manage_bid_url(bid.id, 'detail'))

		self.assertEqual(res.status_code, status.HTTP_200_OK)

		serializer = BidSerializer(bid)

		self.assertEqual(res.data, serializer.data)


	def test_update_bid_by_id(self):
		"""Test update bid by id"""

		task = create_sample_task(creator=self.user)

		bid = create_sample_bid(user=get_user_model().objects.create_user(email='test2@test.com', password='test2pass123', name='test2 man', username='test2man'), task=task)

		payload = {
			'price': 239.00,
		}

		res = self.client.patch(create_manage_bid_url(bid.id, 'detail'), payload)

		bid.refresh_from_db()

		self.assertEqual(res.status_code, status.HTTP_200_OK)

		self.assertEqual(bid.price, payload['price'])



		
