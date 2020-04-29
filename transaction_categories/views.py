from django.core.paginator import EmptyPage, Paginator
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import TransactionCategory
from .serializers import TransactionCategorySerializer
from django.core.exceptions import PermissionDenied

class TransactionCategoriesList(APIView):

	RECORDS_FOR_PAGE = 5

	permission_classes = [
		permissions.IsAuthenticated
	]

	def get(self, request, format=None):

		user = request.user
		num_page = request.GET.get('page', 1)
		paginator = Paginator(user.transaction_categories.order_by('created_at'), self.RECORDS_FOR_PAGE)
		serializer = TransactionCategorySerializer(paginator.page(num_page), many=True)

		return Response({
			'items': serializer.data,
			'num_pages': paginator.num_pages
		})

	def post(self, request, format=None):

		user = request.user
		serializer = TransactionCategorySerializer(data=request.data)

		if serializer.is_valid():

			serializer.save(user=user)
			paginator = Paginator(user.transaction_categories.order_by('created_at'), self.RECORDS_FOR_PAGE)

			return Response({
				'item': serializer.data,
				'num_pages': paginator.num_pages
			}, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionCategoryDetail(APIView):

	RECORDS_FOR_PAGE = 5

	permission_classes = [
		permissions.IsAuthenticated
	]

	def get_transaction_category(self, user, pk):

		try:
			# print(user)
			transaction_category = user.transaction_categories.get(pk=pk)
			return transaction_category
		except TransactionCategory.DoesNotExist:
			raise PermissionDenied

	def get(self, request, pk, format=None):

		transaction_category = self.get_transaction_category(request.user, pk)
		serializer = TransactionCategorySerializer(transaction_category)
		return Response(serializer.data)

	def put(self, request, pk, format=None):

		transaction_category = self.get_transaction_category(request.user, pk)
		serializer = TransactionCategorySerializer(transaction_category, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):

		user = request.user
		transaction_category = self.get_transaction_category(user, pk)
		transaction_category.delete()
		num_page = request.GET.get('page', 1)
		paginator = Paginator(user.transaction_categories.order_by('created_at'), self.RECORDS_FOR_PAGE)
		try:
			transaction_categories = paginator.page(num_page)
		except EmptyPage:
			transaction_categories = []
		serialiazer = TransactionCategorySerializer(transaction_categories, many=True)
		return Response({
			'num_pages': paginator.num_pages,
			'items': serialiazer.data
		}, status=status.HTTP_200_OK)
