from decouple import config
from django.db import migrations
from faker import Faker

from user_accounts.models import UserAccount
from transactions.models import Transaction

def seed_transactions(apps, schema_editor):

	fake = Faker()

	if config('DEBUG', default=False, cast=bool):

		print('Sedding transactions')
		acocunts = UserAccount.objects.all()

		for account in acocunts:

			for i in range(1, 20):

				if fake.pybool():

					account.transactions.create(
						description=fake.text(max_nb_chars=40),
						amount=fake.pyfloat(right_digits=2, positive=True, min_value=2, max_value=30),
						trans_type=Transaction.EXPENSE if fake.pybool() else Transaction.INCOME
					)

def unseed_transactions(apps, schema_editor):
	pass

class Migration(migrations.Migration):

	dependencies = [
		('transactions', '0001_initial'),
	]

	operations = [
		migrations.RunPython(seed_transactions, unseed_transactions)
	]
