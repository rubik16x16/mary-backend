from django.db import models
from user_accounts.models import UserAccount

class Transaction(models.Model):

	INCOME = 'IN'
	EXPENSE = 'EX'

	TYPES_CHOICES = [
		(INCOME, 'Income'),
		(EXPENSE, 'Expense')
	]

	description = models.CharField(max_length=60)
	amount = models.FloatField(max_length=12)
	type = models.CharField(max_length=2, choices=TYPES_CHOICES, default=INCOME)

	account = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='transactions')

	class Meta:
		db_table = 'transactions'
