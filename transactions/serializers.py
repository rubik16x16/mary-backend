from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):

	trans_type = serializers.ChoiceField(choices=Transaction.TYPES_CHOICES, required=True)

	class Meta:
		model = Transaction
		fields = ['id', 'description', 'trans_type', 'amount', 'created_at', 'updated_at']

	def create(self, validated_data):

		return validated_data['account'].transactions.create(**validated_data)

	def update(self, instance, validated_data):

		instance.fill(**validated_data)
		instance.save()
		return instance
