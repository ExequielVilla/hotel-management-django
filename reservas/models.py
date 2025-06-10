from django.db import models
from django.conf import settings
from habitaciones.models import Habitacion, ServicioHab
from usuarios.models import Huesped,User

class Pago(models.Model):
    METODOS = [
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia Bancaria'),
    ]

    metodo_pago = models.CharField(max_length=25, choices=METODOS)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.get_metodo_pago_display()} - ${self.monto_pagado}'
class Reserva(models.Model):
    ESTADOS_RESERVA = [
        ('Pendiente', 'Pendiente'), #color editar
        ('Confirmada', 'Confirmada'), # color agregar
        ('En curso', 'En curso'), #color principal
        ('Cancelada', 'Cancelada'), #color eliminar
        ('Finalizada', 'Finalizada') #color secundary
    ]

    fecha_check_in_esperada = models.DateField()
    fecha_check_out_esperada = models.DateField()
    cantidad_huespedes = models.PositiveIntegerField(default=1)
    habitaciones = models.ManyToManyField(Habitacion)

    huesped = models.ForeignKey(Huesped, on_delete=models.PROTECT, null=False, blank=False)

    monto_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pago = models.OneToOneField(Pago, on_delete=models.PROTECT, null=True, blank=True)

    fecha_check_in_efectuada = models.DateTimeField(null=True, blank=True)
    fecha_check_out_efectuada = models.DateTimeField(null=True, blank=True)

    estado = models.CharField(max_length=15, choices=ESTADOS_RESERVA, default='Pendiente')
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True) #quien hizo la reserva (si es autoreserva, o por el hotel)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reserva {self.id} - {self.huesped or self.usuario}'

    def calcular_total_reserva(self):
        total = sum(habitacion.tipo_habitacion.precio for habitacion in self.habitaciones.all())
        dias = (self.fecha_check_out - self.fecha_check_in).days
        return total * dias if dias > 0 else total

    def esta_pagada(self):
        return self.pago is not None and self.pago.monto_pagado > 0

    def habitaciones_str(self):
        return " - ".join([str(habitacion) for habitacion in self.habitaciones.all()])
    
    def monto_total_str(self):
        return f"${self.monto_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

