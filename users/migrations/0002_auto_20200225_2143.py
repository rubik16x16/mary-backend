from decouple import config
from django.db import migrations
from faker import Faker
from users.models import User


def seed_users(apps, schema_editor):

	User.objects.create_superuser('rubik@rubik.com', 'secret')

	fake = Faker()

	if config('DEBUG', default=False, cast=bool):

		print('Sedding users')
		for i in range(1, 10):

			User.objects.create_user(fake.ascii_email(), 'secret')


def unseed_users(apps, schema_editor):
	pass

class Migration(migrations.Migration):

	dependencies = [
		('users', '0001_initial'),
	]

	operations = [

		migrations.RunPython(seed_users, unseed_users)
	]
