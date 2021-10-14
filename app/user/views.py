from rest_framework import generics, permissions, authentication
from user import serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

class RegisterUserApiView(generics.CreateAPIView):
	"""Register a new user"""
	serializer_class = serializers.UserSerializer


class LoginUserApiView(ObtainAuthToken):
	"""Login user and retrieve an auth token"""
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
	serializer_class = serializers.LoginUserSerializer


class ProfileUserApiView(generics.RetrieveUpdateAPIView):
	"""Get & update a users profile"""

	permission_classes = (permissions.IsAuthenticated, )
	authentication_classes = (authentication.TokenAuthentication, )
	serializer_class = serializers.ProfileUserSerializer

	def get_object(self):
		"""Retrieve and return authenticated user"""
		return self.request.user
