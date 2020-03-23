from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

	initial = True

	dependencies = [
			('user_accounts', '0002_auto_20200225_0214'),
	]

	operations = [
		migrations.CreateModel(
			name='Transaction',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('description', models.CharField(max_length=60)),
				('amount', models.FloatField(max_length=12)),
				('type', models.CharField(choices=[('IN', 'Income'), ('EX', 'Expense')], default='IN', max_length=2)),
				('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='user_accounts.UserAccount')),
				('created_at', models.DateTimeField(auto_now_add=True)),
				('updated_at', models.DateTimeField(auto_now=True))
			],
			options={
				'db_table': 'transactions',
			},
		),
	]
