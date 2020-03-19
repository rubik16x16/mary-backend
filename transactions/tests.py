import random

from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient

from transactions import views
from user_accounts.models import UserAccount
from users.models import User

from .models import Transaction
from .serializers import TransactionSerializer

class TransactionsTestCase(TestCase):

	def setUp(self):

		self.client = APIClient()
		self.fake = Faker()
		self.user = User.objects.first()
		self.account = self.user.accounts.first()
		self.xuser = User.objects.last()
		self.client.force_authenticate(user=self.user)

	def test_list_transactions(self):

		transactions = self.account.transactions.all()
		response = self.client.get(reverse('transactions:list', args=(self.account.id,)), format='json')
		self.assertEqual(len(response.data), len(transactions))

	def test_create_transaction(self):

		data = {
			'description': self.fake.text(max_nb_chars=20),
			'amount': self.fake.pyfloat(right_digits=2, positive=True),
			'type': random.choice(Transaction.TYPES_CHOICES)[0]
		}

		response = self.client.post(reverse('transactions:list', args=(self.account.id,)), data)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Transaction.objects.last().description, data['description'])

	def test_show_transaction(self):

		transaction = self.account.transactions.first()
		serializer = TransactionSerializer(transaction)

		response = self.client.get(reverse('transactions:detail', args=(self.account.id, transaction.id)))

		self.assertEqual(response.data, serializer.data)

	def test_edit_transaction(self):

		data = {
			'description': self.fake.text(max_nb_chars=20),
			'amount': self.fake.pyfloat(right_digits=2, positive=True),
			'type': random.choice(Transaction.TYPES_CHOICES)[0]
		}

		transaction = self.account.transactions.first()
		response = self.client.put(reverse('transactions:detail', args=(self.account.id, transaction.id)), data)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(Transaction.objects.get(pk=transaction.id).description, data['description'])

	def test_delete_transaction(self):

		transaction = self.account.transactions.first()
		response = self.client.delete(reverse('transactions:detail', args=(self.account.id, transaction.id)))

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertNotEqual(transaction.id, self.account.transactions.first().id)
