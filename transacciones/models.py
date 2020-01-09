from django.db import models
from usuarios.models import Usuario

class Transaccion(models.Model):
  descripcion = models.CharField(max_length = 20)
  monto = models.FloatField()
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'transacciones'

  usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='transacciones')