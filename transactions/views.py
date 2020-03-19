from django.http import Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from user_accounts.models import UserAccount

from .models import Transaction
from .serializers import TransactionSerializer

class TransactionsAccountList(APIView):

	permission_classes = [
		permissions.IsAuthenticated
	]

	def get_account(self, user, pk):

		try:
			return user.accounts.get(pk=pk)
		except UserAccount.DoesNotExist:
			raise Http404

	def get(self, request, account_pk, format=None):

		account = self.get_account(request.user, account_pk)
		transactions = account.transactions.all()
		serializer = TransactionSerializer(transactions, many=True)
		return Response(serializer.data)

	def post(self, request, account_pk, format=None):

		account = self.get_account(request.user, account_pk)
		serializer = TransactionSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(account=account)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionsDetail(APIView):

	permission_classes = [
		permissions.IsAuthenticated
	]

	def get_account(self, user, pk):

		try:
			return user.accounts.get(pk=pk)
		except UserAccount.DoesNotExist:
			raise Http404

	def get_transaction(self, account, pk):

		try:
			return account.transactions.get(pk=pk)
		except Transaction.DoesNotExist:
			raise Http404

	def get(self, request, account_pk, pk, format=None):

		account = self.get_account(request.user, account_pk)
		transaction = self.get_transaction(account, pk)
		serializer = TransactionSerializer(transaction)
		return Response(serializer.data)

	def put(self, request, account_pk, pk, format=None):

		account = self.get_account(request.user, account_pk)
		transaction = self.get_transaction(account, pk)
		serializer = TransactionSerializer(transaction, data=request.data)
		if serializer.is_valid():
			serializer.save(account=account)
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, account_pk, pk, format=None):

		account = self.get_account(request.user, account_pk)
		transaction = self.get_transaction(account, pk)
		transaction.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
