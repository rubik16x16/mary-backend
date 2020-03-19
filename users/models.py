from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):

	email = models.CharField(unique=True, max_length=255)

	objects = CustomUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	is_staff = models.BooleanField(
			_('staff status'),
			default=False,
			help_text=_('Designates whether the user can log into this admin site.'),
	)
	is_active = models.BooleanField(
			_('active'),
			default=True,
			help_text=_(
					'Designates whether this user should be treated as active. '
					'Unselect this instead of deleting accounts.'
			),
	)
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

	class Meta:
		db_table = 'users'

	def __str__(self):
		return self.email

	def get_all_permissions(self):

		def assigned(permission, permission_list):

			for item in permission_list:

				if item.name == permission.name:

					return True

			return False

		user_permissions = []
		groups = self.groups.all()

		for group in groups:

			group_permissions = group.permissions.all()

			for permission in group_permissions:

				if not assigned(permission, user_permissions):

					user_permissions.append(permission)

		return user_permissions

	@staticmethod
	def get_random():

		return User.objects.order_by("?").first()
