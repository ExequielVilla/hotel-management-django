# Generated by Django 5.0.6 on 2025-04-03 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0002_reserva_activo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='cantidad_huespedes',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
