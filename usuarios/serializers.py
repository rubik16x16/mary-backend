from rest_framework import serializers
from usuarios.models import Usuario
from django.contrib.auth.models import Permission

# class PermissionsSerializer(serializers.ModelSerializer):

#   class Meta:
#     model = Permission
#     fields = ['name', 'codename']

class UsuarioSerializer(serializers.ModelSerializer):

  permissions = serializers.StringRelatedField(many=True)

  class Meta:
    model = Usuario
    fields = ['email', 'permissions']