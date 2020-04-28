from django.db import models
from user_accounts.models import UserAccount
from tools.mary_model import MaryModel

class Transaction(models.Model, MaryModel):

	INCOME = 'IN'
	EXPENSE = 'EX'

	TYPES_CHOICES = [
		(INCOME, 'Income'),
		(EXPENSE, 'Expense')
	]

	description = models.CharField(max_length=60)
	amount = models.FloatField(max_length=12)
	trans_type = models.CharField(max_length=2, choices=TYPES_CHOICES, default=INCOME)

	account = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='transactions')

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'transactions'
