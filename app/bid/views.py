from rest_framework.views import APIView
from core.models import Task, Bid
from rest_framework import status, permissions, authentication, viewsets, mixins
from rest_framework.response import Response
from bid import serializers
class ListCreateBidApiView(APIView):
	"""Create & list bid model related to task"""

	serializer_class = serializers.BidSerializer
	authentication_classes = (authentication.TokenAuthentication, )
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

	def post(self, request, id, *args, **kwargs):
		"""Create an order in the system"""

		# find the task with id
		task = Task.objects.get(id=id)

		if task is None:
			# if not task is found with the id return a 404
			return Response({'detail': 'The task with id {id} was not found'}, status.HTTP_404_NOT_FOUND)

		# TODO --> fix task creator bid 
		if task.creator is self.request.user:
			# check if creator of task
			return Response({'detail': 'Creator of task cannot set bid'}, status.HTTP_400_BAD_REQUEST) 

		serializer = self.serializer_class(data=request.data)	
		if serializer.is_valid():
			serializer.save(task=task, user=self.request.user)

			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	def get(self, request, id,  format=None):
		"""Get the bids associated with an order"""

		#  find the task
		task = Task.objects.get(id=id)

		if task is None:
			return Response({'detail': 'The task with id {id} was not found'}, status.HTTP_404_NOT_FOUND)

		bids = Bid.objects.filter(task=task)

		serializer = self.serializer_class(bids, many=True)

		return Response(serializer.data, status=status.HTTP_200_OK)


class BidView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
	"""Retrieve, Delete and Update Bids viewset"""

	authentication_classes = (authentication.TokenAuthentication, )
	permission_classes = (permissions.IsAuthenticated, )
	queryset = Bid.objects.all()
	serializer_class = serializers.BidSerializer





