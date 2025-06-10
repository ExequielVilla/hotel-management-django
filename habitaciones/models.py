from django.db import models

class ServicioHab(models.Model):
    nombre = models.CharField(max_length=100)
    icono = models.CharField(max_length=50, default='fa-check') #Nombre del icono de FontAwesome
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
    nombre = models.CharField(max_length=30)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    capacidad_maxima = models.PositiveIntegerField(default=1)
    servicios = models.ManyToManyField(ServicioHab)
    fotos = models.ManyToManyField(FotoHabitacion, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class TipoCama(models.TextChoices):
    KING = 'King'
    DOUBLE = 'Double'
    TWIN = 'Twin'

class CamaTipoHabitacion(models.Model):
    tipo_habitacion = models.ForeignKey('TipoHabitacion', on_delete=models.CASCADE)
    tipo_cama = models.CharField(max_length=10, choices=TipoCama.choices)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cantidad} cama(s) {self.get_tipo_cama_display()} - {self.tipo_habitacion.nombre}"


class Habitacion(models.Model):
    ESTADO_HABITACION = [ #estado ACTUAL de ESE DIA en ESE MOMENTO/HORA
        ('Habilitada', 'Habilitada'), #Habilitada no significa que esté disponible sin reservas, sino solo lista para ser utilizada. Ya que la disponibilidad depende de la fecha
        ('Ocupada', 'Ocupada'),
        ('En limpieza', 'En Limpieza'),
    ]
    numero = models.CharField(max_length=3, unique=True)
    tipo_habitacion = models.ForeignKey(TipoHabitacion, on_delete=models.PROTECT)
    estado = models.CharField(max_length=20, choices=ESTADO_HABITACION, default='Disponible')
    activo = models.BooleanField(default=True) 

    def __str__(self):
        return f'N°{self.numero} {self.tipo_habitacion.nombre}'