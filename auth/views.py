from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import UserSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
	# @classmethod
	# def get_token(cls, user):
	#   token = super().get_token(user)

	#   # Add custom claims
	#   token['email'] = user.email
	#   # ...

	#   return token

	def create(self, validated_data):
		pass

	def update(self, instance, validated_data):
		pass

	def validate(self, attrs):
		data = super().validate(attrs)

		refresh = self.get_token(self.user)

		data['refresh'] = str(refresh)
		data['access'] = str(refresh.access_token)

		user = self.user
		user.permissions = user.get_all_permissions()
		usuario_serializer = UserSerializer(user)
		data['user'] = usuario_serializer.data

		return data

class MyTokenObtainPairView(TokenObtainPairView):
	serializer_class = MyTokenObtainPairSerializer
