# Generated by Django 3.0.3 on 2020-02-25 21:43

from django.db import migrations
from usuarios.models import Usuario as User

def seed_users(apps, schema_editor):

  User.objects.create_superuser('rubik@rubik.com', 'secret')


def unseed_users(apps, schema_editor):
  pass

class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [

      migrations.RunPython(seed_users, unseed_users)
    ]
