from django.db import migrations, models
import django.db.models.deletion
import tools.mary_model

class Migration(migrations.Migration):

	initial = True

	dependencies = [
		('users', '0002_auto_20200225_2143'),
	]

	operations = [
		migrations.CreateModel(
			name='TransactionCategory',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('name', models.CharField(max_length=20)),
				('created_at', models.DateTimeField(auto_now_add=True)),
				('updated_at', models.DateTimeField(auto_now=True)),
				('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_categories', to='users.User')),
			],
			options={
				'db_table': 'transaction_categories',
			},
			bases=(models.Model, tools.mary_model.MaryModel),
		),
	]
