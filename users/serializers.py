from django.contrib.auth.models import Permission
from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ['email', 'user_permissions']
