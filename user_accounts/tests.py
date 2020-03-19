from django.test import TestCase
from faker import Faker
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from user_accounts.views import UserAccountsDetail, UserAccountsList
from users.models import User

class UserAccountTestCase(TestCase):

	user_accounts_len = 2

	def setUp(self):

		self.factory = APIRequestFactory()
		self.fake = Faker()
		self.user = User.objects.create_user('test@g.com', 'secret')
		self.xuser = User.objects.create_user('test2@g.com', 'secret')
		for i in range(0, self.user_accounts_len):

			self.user.accounts.create(
				name=self.fake.text(max_nb_chars=20),
				amount=self.fake.pyfloat(right_digits=2, positive=True, min_value=300, max_value=1200)
			)

			self.xuser.accounts.create(
				name=self.fake.text(max_nb_chars=20),
				amount=self.fake.pyfloat(right_digits=2, positive=True, min_value=300, max_value=1200)
			)

	def test_list_user_accounts(self):

		view = UserAccountsList.as_view()
		request = self.factory.get('/user/accounts')
		force_authenticate(request, user=self.user)
		response = view(request)
		self.assertEqual(len(response.data), self.user_accounts_len)

	def test_create_user_accounts(self):

		data = {
			'name': 'test',
			'amount': 500
		}
		view = UserAccountsList.as_view()
		request = self.factory.post('/user/accounts', data)
		force_authenticate(request, user=self.user)
		response = view(request)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_show_user_account(self):

		user_account = self.user.accounts.first()
		view = UserAccountsDetail.as_view()
		request = self.factory.get('/user/accounts/%d' % user_account.id)
		force_authenticate(request, user=self.user)
		response = view(request, user_account.id)
		self.assertEqual(user_account.id, response.data['id'])

	def test_edit_user_account(self):

		# Bad request
		data = {
			'name': 'test',
			'amount': 500
		}

		xuser = User.objects.get(email='test2@g.com')
		user_account = xuser.accounts.order_by('?').first()
		view = UserAccountsDetail.as_view()
		request = self.factory.put('/user/accounts/%d' % user_account.id, data)
		force_authenticate(request, user=self.user)
		response = view(request, user_account.id)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

		# Good request

		user_account = self.user.accounts.order_by('?').first()
		request = self.factory.put('/user/accounts/%d' % user_account.id, data)
		force_authenticate(request, user=self.user)
		response = view(request, user_account.id)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_delete_user_account(self):

		# Bad request

		xuser = User.objects.get(email='test2@g.com')
		user_account = xuser.accounts.order_by('?').first()
		view = UserAccountsDetail.as_view()
		request = self.factory.delete('/user/accounts/%d' % user_account.id)
		force_authenticate(request, user=self.user)
		response = view(request, user_account.id)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

		# Good request

		user_account = self.user.accounts.order_by('?').first()
		request = self.factory.delete('/user/accounts/%d' % user_account.id)
		force_authenticate(request, user=self.user)
		response = view(request, user_account.id)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
