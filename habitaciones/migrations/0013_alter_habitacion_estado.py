# Generated by Django 5.0.6 on 2025-03-12 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habitaciones', '0012_alter_habitacion_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habitacion',
            name='estado',
            field=models.CharField(choices=[('Disponible', 'Disponible'), ('Ocupada', 'Ocupada'), ('En limpieza', 'En Limpieza'), ('Mantenimiento', 'En Mantenimiento'), ('Reservada', 'Reservada')], default='Disponible', max_length=20),
        ),
    ]
