import random

from django.core.paginator import Paginator
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
from .views import TransactionsList, TransactionsDetail

class TransactionsTestCase(TestCase):

	def setUp(self):

		self.client = APIClient()
		self.fake = Faker()
		self.user = User.objects.first()
		self.account = self.user.accounts.first()
		self.xuser = User.objects.last()
		self.client.force_authenticate(user=self.user)

	def test_list_transactions(self):

		paginator = Paginator(self.account.transactions.order_by('created_at'), TransactionsList.RECORDS_FOR_PAGE)
		url = reverse('transactions:list', args=(self.account.id,))
		response = self.client.get(url, format='json')
		self.assertEqual(len(response.data['items']), len(paginator.page(1)))

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
		response = self.client.get(reverse('transactions:detail', args=(transaction.id,)))

		self.assertEqual(response.data, serializer.data)

	def test_edit_transaction(self):

		data = {
			'description': self.fake.text(max_nb_chars=20),
			'amount': self.fake.pyfloat(right_digits=2, positive=True),
			'type': random.choice(Transaction.TYPES_CHOICES)[0]
		}

		transaction = self.account.transactions.first()
		response = self.client.put(reverse('transactions:detail', args=(transaction.id,)), data)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(Transaction.objects.get(pk=transaction.id).description, data['description'])

	def test_delete_transaction(self):

		transaction = self.account.transactions.first()
		response = self.client.delete(reverse('transactions:detail', args=(transaction.id,)))

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertNotEqual(transaction.id, self.account.transactions.first().id)

	def test_security(self):

		# Authorized
		self.client.logout()
		response = self.client.get(reverse('transactions:list', args=(self.account.id,)), format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		response = self.client.get(reverse('transactions:detail', args=(1,)), format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

		# list Own transactions
		account = self.user.accounts.first()
		self.client.force_authenticate(self.xuser)
		response = self.client.get(reverse('transactions:list', args=(account.id,)), format='json')
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

		# Create transaction on own account
		response = self.client.post(reverse('transactions:list', args=(account.id,)), format='json')
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

		# See own transactions
		transaction = self.account.transactions.first()
		response = self.client.get(reverse('transactions:detail', args=(transaction.id,)))
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

		# Update own transaction
		response = self.client.put(reverse('transactions:detail', args=(transaction.id,)))
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

		#delete own transaction
		response = self.client.delete(reverse('transactions:detail', args=(transaction.id,)))
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
