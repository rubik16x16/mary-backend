from django.db import models
from users.models import User

class UserAccount(models.Model):

	name = models.CharField(max_length=20)
	amount = models.FloatField(max_length=12)

	class Meta:
		db_table = 'user_accounts'

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')

	@staticmethod
	def get_random():

		return User.objects.order_by("?").first()
