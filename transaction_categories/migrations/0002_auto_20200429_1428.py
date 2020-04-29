from django.db import migrations
from decouple import config
from faker import Faker
from users.models import User

def seed_transaction_categories(apps, schema_editor):

	fake = Faker()

	if config('SEED', default=False, cast=bool):

		print('Sedding transaction_categories')
		users = User.objects.all()

		for user in users:

			for i in range(1, 5):

				user.transaction_categories.create(
					name=fake.text(max_nb_chars=20),
				)

def unseed_transaction_categories(apps, schema_editor):
	pass


class Migration(migrations.Migration):

	dependencies = [
		('transaction_categories', '0001_initial'),
	]

	operations = [
		migrations.RunPython(seed_transaction_categories, unseed_transaction_categories)
	]
