from rest_framework import serializers

from .models import TransactionCategory

class TransactionCategorySerializer(serializers.ModelSerializer):

	class Meta:

		model = TransactionCategory
		fields = ['name', 'created_at', 'updated_at']

	def create(self, validated_data):

		user = validated_data['user']

		return user.transaction_categories.create(**validated_data)
