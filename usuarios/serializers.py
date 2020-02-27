from rest_framework import serializers
from usuarios.models import Usuario
from django.contrib.auth.models import Permission

class UsuarioSerializer(serializers.ModelSerializer):

  class Meta:
    model = Usuario
    fields = ['email', 'user_permissions']