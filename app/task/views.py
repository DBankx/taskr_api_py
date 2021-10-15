from task.permissions import UpdateOwnTask
from core.models import Task
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from task import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class TaskViewSet(viewsets.ModelViewSet):
	"""Manage Task in the db"""

	serializer_class = serializers.TaskSerializer
	permission_classes = (IsAuthenticatedOrReadOnly, UpdateOwnTask, )
	authentication_classes = (TokenAuthentication, )
	queryset = Task.objects.all()


	def perform_create(self, serializer):
		"""Create a task view set"""

		return serializer.save(creator=self.request.user)

	def get_queryset(self):
		"""Retrieve all tasks"""

		return self.queryset.order_by('-created_at')

	def get_serializer_class(self):
		"""Retrieve correct serializer class"""

		if self.action == 'retrieve':
			return serializers.TaskDetailSerializer

		return self.serializer_class		

	@action(methods=['GET'], detail=False, url_path='my-tasks', url_name='my-tasks')
	def view_owned_tasks(self, request):
		"""Get tasks owned by the current user"""

		serializer = self.get_serializer(self.queryset.filter(creator=request.user).order_by('-created_at'), many=True)

		return Response(serializer.data, status=status.HTTP_200_OK)


	


