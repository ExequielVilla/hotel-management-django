from rest_framework import serializers
from usuarios.models import Huesped

class HuespedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Huesped
        fields = ['id', 'nombre', 'apellido', 'dni_pasaporte', 'email', 'telefono', 'preferencias']