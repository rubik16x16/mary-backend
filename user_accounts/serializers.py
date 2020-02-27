from rest_framework import serializers
from user_accounts.models import UserAccount
from usuarios.serializers import UsuarioSerializer as UserSerializer

class  UserAccountSerializer(serializers.ModelSerializer):

  user = serializers.StringRelatedField(allow_null=True)

  class Meta:
    model = UserAccount
    fields = ['id', 'name', 'amount', 'user']

  def create(self, validated_data):

    return validated_data['user'].accounts.create(**validated_data)
