from django.db import models
from tools.mary_model import MaryModel
from users.models import User

class TransactionCategory(models.Model, MaryModel):

	name = models.CharField(max_length=20)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction_categories')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'transaction_categories'
