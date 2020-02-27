from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.http import Http404

from user_accounts.models import UserAccount
from user_accounts.serializers import UserAccountSerializer

class UserAccountsList(APIView):

  permission_classes = [
    permissions.IsAuthenticated
  ]

  def get(self, request, format=None):

    user = request.user
    user_accounts = user.accounts.all()
    serializer = UserAccountSerializer(user_accounts, many=True)
    return Response(serializer.data)

  def post(self, request, formart=None):

    serializer = UserAccountSerializer(data = request.data)
    if serializer.is_valid():
      serializer.save(user=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAccountsDetail(APIView):

  permission_classes = [
    permissions.IsAuthenticated
  ]

  def get_object(self, pk, user):

    try:
      return user.accounts.get(pk = pk)
    except UserAccount.DoesNotExist:
      raise Http404

  def get(self, request, pk, format=None):

    user_account = self.get_object(pk, request.user)
    serializer = UserAccountSerializer(user_account)
    return Response(serializer.data)

  def put(self, request, pk, format=None):

    user_account = self.get_object(pk, request.user)
    serializer = UserAccountSerializer(user_account, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):

    user_account = self.get_object(pk, request.user)
    user_account.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
