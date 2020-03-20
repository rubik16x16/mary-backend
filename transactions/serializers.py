from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):

	class Meta:
		model = Transaction
		fields = ['id', 'description', 'type', 'amount']

	def create(self, validated_data):

		return validated_data['account'].transactions.create(**validated_data)

	def update(self, instance, validated_data):

		instance.fill(**validated_data)
		instance.save()
		return instance
