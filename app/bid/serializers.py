from core.models import Bid
from rest_framework import serializers

class BidSerializer(serializers.ModelSerializer):
	"""Serializer for creating bid"""

	class Meta:
		model = Bid
		fields = ('id', 'task', 'description', 'price', 'status', 'user', 'created_at', 'updated_at')
		read_only_fields = ('id', 'status', 'updated_at', 'created_at', 'task', 'user' )

