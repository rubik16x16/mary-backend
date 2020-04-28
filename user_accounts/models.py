from django.db import models
from users.models import User

class UserAccount(models.Model):

	name = models.CharField(max_length=20)
	amount = models.FloatField(max_length=12)

	class Meta:
		db_table = 'user_accounts'

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	@staticmethod
	def get_random():

		return UserAccount.objects.order_by("?").first()
