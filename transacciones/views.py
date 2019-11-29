from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.http import Http404

from transacciones.models import Transaccion
from transacciones.serializers import TransaccionSerializer

from usuarios.serializers import UsuarioSerializer

class TransaccionesList(APIView):

  permission_classes = [
    permissions.IsAuthenticated
  ]

  def get(self, request, format=None):

    transacciones = Transaccion.objects.all()
    serializer = TransaccionSerializer(transacciones, many=True)
    return Response(serializer.data)

  def post(self, request, formart=None):

    serializer = TransaccionSerializer(data = request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransaccionesDetail(APIView):

  permission_classes = [permissions.IsAuthenticatedOrReadOnly]

  def get_object(self, pk):
    try:
      return Transaccion.objects.get(pk = pk)
    except Transaccion.DoesNotExist:
      raise Http404

  def get(self, request, pk, format=None):
    transaccion = self.get_object(pk)
    serializer = TransaccionSerializer(transaccion)
    return Response(serializer.data)

  def put(self, request, pk, format=None):
    transaccion = self.get_object(pk)
    serializer = TransaccionSerializer(transaccion, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    transaccion = self.get_object(pk)
    transaccion.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)