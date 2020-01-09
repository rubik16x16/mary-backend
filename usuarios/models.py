from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

from .managers import CustomUserManager

class Usuario(AbstractUser):

  email = models.CharField(unique=True, max_length=255)

  objects = CustomUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  class Meta:
    db_table = 'usuarios'

  def __str__(self):
    return self.email

  def get_all_permissions(self):

    def asignado(permission, permission_list):

      for item in permission_list:

        if item.name == permission.name:

          return True

      return False

    user_permissions = []
    groups = self.groups.all()

    for group in groups:

      group_permissions = group.permissions.all()

      for permission in group_permissions:

        if not asignado(permission, user_permissions):

          user_permissions.append(permission)

    return user_permissions

  @staticmethod
  def get_random():

    return Usuario.objects.order_by("?").first()
