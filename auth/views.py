from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from usuarios.serializers import UsuarioSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  # @classmethod
  # def get_token(cls, user):
  #   token = super().get_token(user)

  #   # Add custom claims
  #   token['email'] = user.email
  #   # ...

  #   return token

  def validate(self, attrs):
    data = super().validate(attrs)

    refresh = self.get_token(self.user)

    data['refresh'] = str(refresh)
    data['access'] = str(refresh.access_token)

    user = self.user
    user.permissions = user.get_all_permissions()
    usuario_serializer = UsuarioSerializer(user)
    data['user'] = usuario_serializer.data

    return data

class MyTokenObtainPairView(TokenObtainPairView):
  serializer_class = MyTokenObtainPairSerializer
