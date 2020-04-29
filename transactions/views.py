from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from user_accounts.models import UserAccount

from .models import Transaction
from .serializers import TransactionSerializer

class TransactionsList(APIView):

	RECORDS_FOR_PAGE = 5

	permission_classes = [
		permissions.IsAuthenticated
	]

	def get_account(self, user, pk):

		try:
			return user.accounts.get(pk=pk)
		except UserAccount.DoesNotExist:
			raise PermissionDenied

	def get(self, request, account_pk, format=None):

		account = self.get_account(request.user, account_pk)
		num_page = request.GET.get('page', 1)
		paginator = Paginator(account.transactions.order_by('-created_at'), self.RECORDS_FOR_PAGE)
		serializer = TransactionSerializer(paginator.page(num_page), many=True)

		return Response({
			'items': serializer.data,
			'num_pages': paginator.num_pages
		})

	def post(self, request, account_pk, format=None):

		account = self.get_account(request.user, account_pk)
		serializer = TransactionSerializer(data=request.data)

		if serializer.is_valid():

			serializer.save(account=account)
			paginator = Paginator(account.transactions.order_by('created_at'), self.RECORDS_FOR_PAGE)

			return Response({
				'item': serializer.data,
				'num_pages': paginator.num_pages
			}, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionsDetail(APIView):

	permission_classes = [
		permissions.IsAuthenticated
	]

	RECORDS_FOR_PAGE = 5

	def get_transaction(self, user, pk):

		try:
			transaction = Transaction.objects.get(pk=pk)
			account = user.accounts.get(pk=transaction.account.id)
			return account.transactions.get(pk=pk)
		except UserAccount.DoesNotExist:
			raise PermissionDenied
		except Transaction.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):

		transaction = self.get_transaction(request.user, pk)
		serializer = TransactionSerializer(transaction)
		return Response(serializer.data)

	def put(self, request, pk, format=None):

		transaction = self.get_transaction(request.user, pk)
		serializer = TransactionSerializer(transaction, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):

		transaction = self.get_transaction(request.user, pk)
		transaction.delete()
		num_page = request.GET.get('page', 1)
		paginator = Paginator(transaction.account.transactions.order_by('-created_at'), self.RECORDS_FOR_PAGE)
		try:
			transactions = paginator.page(num_page)
		except EmptyPage:
			transactions = []
		serialiazer = TransactionSerializer(transactions, many=True)
		return Response({
			'num_pages': paginator.num_pages,
			'items': serialiazer.data
		}, status=status.HTTP_200_OK)
