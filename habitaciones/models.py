from django.db import models

class ServicioHab(models.Model):
    nombre = models.CharField(max_length=100)
    icono = models.CharField(max_length=50) #Nombre del icono de FontAwesome o Material Icons
    activo = models.BooleanField(default=True) 

    def __str__(self):
        return self.nombre


class FotoHabitacion(models.Model):
    imagen = models.ImageField(upload_to='fotos_habitaciones/')

    def __str__(self):
        return f"Foto {self.id}"

    class Meta:
        ordering = ['id']  # Ordenar por ID para mantener secuencia lógica


class TipoHabitacion(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    capacidad_maxima = models.IntegerField(default=1)
    servicios = models.ManyToManyField(ServicioHab)
    fotos = models.ManyToManyField(FotoHabitacion, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Habitacion(models.Model):
    ESTADO_HABITACION = [
        ('Disponible', 'Disponible'),
        ('Ocupada', 'Ocupada'),
        ('En limpieza', 'En Limpieza'),
        ('Mantenimiento', 'En Mantenimiento'),
        ('Reservada', 'Reservada'),
    ]
    numero = models.CharField(max_length=3, unique=True)
    tipo_habitacion = models.ForeignKey(TipoHabitacion, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADO_HABITACION, default='Disponible')
    activo = models.BooleanField(default=True) 

    def __str__(self):
        return f'Habitación {self.numero} - {self.tipo_habitacion.nombre}'