# Generated by Django 5.0.6 on 2024-08-18 02:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('habitaciones', '0002_remove_habitacion_capacidad_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Caracteristica',
            new_name='CaracteristicaHab',
        ),
    ]
