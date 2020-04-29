from django.db import transaction as DbTransaction
from rest_framework import serializers

from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):

	trans_type = serializers.ChoiceField(choices=Transaction.TYPES_CHOICES, required=True)

	class Meta:
		model = Transaction
		fields = ['id', 'description', 'trans_type', 'amount', 'created_at', 'updated_at']

	def create(self, validated_data):

		account = validated_data['account']

		with DbTransaction.atomic():

			if validated_data['trans_type'] == Transaction.INCOME:
				account.amount += validated_data['amount']
			else:
				account.amount -= validated_data['amount']
			account.save()

			transaction = account.transactions.create(**validated_data)

		return transaction

	def update(self, instance, validated_data):

		instance.fill(**validated_data)
		instance.save()
		return instance
