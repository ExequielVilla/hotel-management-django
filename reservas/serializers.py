from rest_framework import serializers
from habitaciones.models import TipoHabitacion, CamaTipoHabitacion
from babel.numbers import format_currency

class TipoHabitacionDisponibilidadSerializer(serializers.ModelSerializer):
    cant_disponibles = serializers.IntegerField()
    precio_texto = serializers.SerializerMethodField()
    camas_texto = serializers.SerializerMethodField()
    servicios_texto = serializers.SerializerMethodField()


    class Meta:
        model = TipoHabitacion
        fields = ['id', 'nombre', 'precio', 'capacidad_maxima', 'cant_disponibles', 'precio_texto', 'camas_texto', 'servicios_texto']

    def get_precio_texto(self, obj):
        precio_str = format_currency(obj.precio, 'ARS', locale='es_AR')
        return f"{precio_str}"
        #return f"{obj.nombre} - {precio_str} p/noche - Cap. {obj.capacidad_maxima} pers."

    def get_camas_texto(self, obj):
        camas = obj.camatipohabitacion_set.all()
        return ", ".join([f"{cama.get_tipo_cama_display()} ({cama.cantidad})" for cama in camas])

    def get_servicios_texto(self, obj):
        return ", ".join([servicio.nombre for servicio in obj.servicios.all()])