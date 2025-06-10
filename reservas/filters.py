import django_filters
from django import forms
from .models import Reserva


class ReservaFilter(django_filters.FilterSet):
    estado = django_filters.ChoiceFilter(
        choices=[
            ('Pendiente', 'Pendiente'),
            ('Confirmada', 'Confirmada'),
            ('Cancelada', 'Cancelada'),
            ('Finalizada', 'Finalizada'),
        ],
        label='Estado',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Reserva
        fields = ['estado']