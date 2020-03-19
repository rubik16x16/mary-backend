from rest_framework import serializers
from users.serializers import UserSerializer
from .models import UserAccount

class  UserAccountSerializer(serializers.ModelSerializer):

	# user = serializers.StringRelatedField(allow_null=True)

	class Meta:
		model = UserAccount
		fields = ['id', 'name', 'amount']

	def create(self, validated_data):

		return validated_data['user'].accounts.create(**validated_data)
