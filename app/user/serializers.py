from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _

class UserSerializer(serializers.ModelSerializer):
	"""Serializer for the user db model"""

	class Meta:
		model = get_user_model()
		fields = ('email', 'password', 'name')
		extra_kwargs = {
			'password': {
				'write_only': True,
				'min_length': 8
			},

		}

	def create(self, validated_data):
		"""create a new user with encrypted password"""

		return get_user_model().objects.create_user(**validated_data)

class LoginUserSerializer(serializers.Serializer):
	"""serializer for the authentication process"""

	email = serializers.CharField()
	password = serializers.CharField(style={'input-type': 'password'}, trim_whitespace=False, )

	def validate(self, attrs):
		"""Validate the authenticated user"""
		email = attrs.get('email')
		password = attrs.get('password')

		user = authenticate(request=self.context.get('request'), email=email, password=password)

		if not user:
			msg = _('Unable to authenticate with provided credentials')
			raise serializers.ValidationError(msg, code='authentication')

		attrs['user'] = user

		return attrs	

class ProfileUserSerializer(serializers.ModelSerializer):
	"""Serializer to return profile of a user"""

	class Meta:
		model = get_user_model()
		fields = ('id', 'email', 'name', 'bio', 'country', 'is_email_verified', 'is_phone_verified', 'phone', 'username', 'avatar', 'has_on_boarded')
		read_only_fields = ('id', 'is_phone_verified', 'username', 'is_email_verified', 'has_on_boarded', 'name', 'phone', 'email')

		
class UserDetailModelSerializer(serializers.ModelSerializer):
	"""Serializer to return user object with models"""

	class Meta:
		model = get_user_model()
		fields = ('id', 'email', 'username', 'avatar')
		read_only_fields = ('id', )		