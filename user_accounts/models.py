from django.db import models
from usuarios.models import Usuario

class UserAccount(models.Model):

  name = models.CharField(max_length=20)
  amount = models.FloatField(max_length=12)

  class Meta:
    db_table = 'user_accounts'

  user = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='accounts')

  @staticmethod
  def get_random():

    return Usuario.objects.order_by("?").first()
