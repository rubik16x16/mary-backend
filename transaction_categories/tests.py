from django.core.paginator import Paginator
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient

from transactions import views
from user_accounts.models import UserAccount
from users.models import User

from .models import TransactionCategory
from .serializers import TransactionCategorySerializer
from .views import TransactionCategoriesList

class TransactionCategoriesTestCase(TestCase):

	def setUp(self):

		self.client = APIClient()
		self.fake = Faker()
		self.user = User.objects.first()
		self.xuser = User.objects.last()
		self.client.force_authenticate(user=self.user)

	def test_list_transaction_categories(self):

		paginator = Paginator(self.user.transaction_categories.order_by('created_at'), TransactionCategoriesList.RECORDS_FOR_PAGE)
		url = reverse('user:transaction_categories:list')
		response = self.client.get(url, format='json')
		self.assertEqual(len(response.data['items']), len(paginator.page(1)))

	def test_create_transaction_category(self):

		data = {
			'name': self.fake.text(max_nb_chars=20),
		}

		response = self.client.post(reverse('user:transaction_categories:list'), data)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(TransactionCategory.objects.last().name, data['name'])

	def test_show_transaction_category(self):

		transaction_category = self.user.transaction_categories.first()
		serializer = TransactionCategorySerializer(transaction_category)
		response = self.client.get(reverse('user:transaction_categories:detail', args=(transaction_category.id,)))

		self.assertEqual(response.data, serializer.data)

	def test_edit_transaction_category(self):

		data = {
			'name': self.fake.text(max_nb_chars=20)
		}

		transaction_category = self.user.transaction_categories.first()
		response = self.client.put(reverse('user:transaction_categories:detail', args=(transaction_category.id,)), data)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(TransactionCategory.objects.get(pk=transaction_category.id).name, data['name'])

	def test_delete_transaction_category(self):

		transaction_category = self.user.transaction_categories.first()
		response = self.client.delete(reverse('user:transaction_categories:detail', args=(transaction_category.id,)))

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertNotEqual(transaction_category.id, self.user.transaction_categories.first().id)

	def test_security(self):

		# Authorized
		self.client.logout()
		response = self.client.get(reverse('user:transaction_categories:list'), format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		response = self.client.get(reverse('user:transaction_categories:detail', args=(1,)), format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

		self.client.force_authenticate(self.xuser)
		# See own transaction_categories
		transaction_category = self.user.transaction_categories.first()
		response = self.client.get(reverse('user:transaction_categories:detail', args=(transaction_category.id,)))
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

		# Update own transaction_categories
		response = self.client.put(reverse('user:transaction_categories:detail', args=(transaction_category.id,)))
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

		#delete own transaction_categories
		response = self.client.delete(reverse('user:transaction_categories:detail', args=(transaction_category.id,)))
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
