from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver

@receiver(post_migrate)
def crear_grupos_y_permisos(sender, **kwargs):
    if sender.name == "usuarios":  # Asegura que solo se ejecuta en esta app
        grupos = ["Administrador", "Recepcionista", "Huesped"]
        for grupo_nombre in grupos:
            Group.objects.get_or_create(name=grupo_nombre)

        # Asignar permisos específicos
        permisos_admin = Permission.objects.all()  # Admin tiene todos
        permisos_recepcionista = Permission.objects.filter(content_type__model="habitacion").exclude(codename__startswith="add_").exclude(codename__startswith="delete_").exclude(codename__startswith="change_")
        admin_group = Group.objects.get(name="Administrador")
        recepcionista_group = Group.objects.get(name="Recepcionista")
        admin_group.permissions.set(permisos_admin)
        recepcionista_group.permissions.set(permisos_recepcionista)
