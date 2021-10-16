from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.models import Task
from user.serializers import UserDetailModelSerializer

class TaskSerializer(serializers.ModelSerializer):
	"""Serializer class for task model"""

	creator = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

	class Meta:
		model = Task
		fields = ('id', 'title', 'description', 'price', 'creator', 'delivery_date', 'created_at', 'status')
		read_only_fields = ('id', )

class TaskDetailSerializer(TaskSerializer):
	"""Serializer for detailing a task"""

	creator = UserDetailModelSerializer(read_only=True)

