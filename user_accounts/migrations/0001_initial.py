from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

	initial = True

	dependencies = [
	]

	operations = [
		migrations.CreateModel(
			name='UserAccount',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('name', models.CharField(max_length=20)),
				('amount', models.FloatField(max_length=12)),
				('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='users.User')),
				('created_at', models.DateTimeField(auto_now_add=True)),
				('updated_at', models.DateTimeField(auto_now=True))
			],
			options={
				'db_table': 'user_accounts',
			},
		),
	]
