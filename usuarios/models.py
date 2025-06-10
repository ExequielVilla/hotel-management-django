from django.contrib.auth.models import User
from django.db import models

# class CustomUser(AbstractUser):
#     # telefono = models.CharField(max_length=15, blank=True, null=True)
#     # localidad = models.CharField(max_length=50)
#     # pais = models.CharField(max_length=50)
#     groups = models.ManyToManyField(
#         Group,
#         related_name="customuser_groups",  # Cambia el related_name
#         blank=True
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name="customuser_permissions",  # Cambia el related_name
#         blank=True
#     )

#     def __str__(self):
#         return self.username

#     def es_admin(self):
#         return self.groups.filter(name="Administrador").exists()

#     def es_recepcionista(self):
#         return self.groups.filter(name="Recepcionista").exists()

#     def es_huesped(self):
#         return self.groups.filter(name="Huesped").exists()

class Huesped(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=50)
    dni_pasaporte = models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    preferencias = preferencias = models.TextField(blank=True, null=True)
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.dni_pasaporte}"