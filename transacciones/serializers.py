from rest_framework import serializers
from transacciones.models import Transaccion

class TransaccionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Transaccion
    fields = ['nombre', 'monto']