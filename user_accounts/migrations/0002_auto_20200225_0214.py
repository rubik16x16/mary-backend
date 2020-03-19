from decouple import config
from django.db import migrations
from faker import Faker

from user_accounts.models import UserAccount
from users.models import User

def seed_user_accounts(apps, schema_editor):

	fake = Faker()

	if config('DEBUG', default=False, cast=bool):

		print('Sedding user accounts')

		users = User.objects.all()

		for user in users:

			for i in range(1, 2):

				user.accounts.create(
					name=fake.text(max_nb_chars=20),
					amount=fake.pyfloat(right_digits=2, positive=True, min_value=300, max_value=1200)
				)

def unseed_user_accounts(apps, schema_editor):
	pass

class Migration(migrations.Migration):

	dependencies = [
		('user_accounts', '0001_initial'),
		('users', '0002_auto_20200225_2143')
	]

	operations = [
		migrations.RunPython(seed_user_accounts, unseed_user_accounts)
	]
