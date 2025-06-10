from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Reserva, Pago
from usuarios.models import Huesped
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import inlineformset_factory
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.utils import timezone 
from django.core.exceptions import ValidationError


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['metodo_pago']
        widgets = {
            'metodo_pago': forms.Select(attrs={'class': 'form-select'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['metodo_pago'].choices = [('', 'Pendiente de pago')] + Pago.METODOS
        self.fields['metodo_pago'].required=False

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha_check_in_esperada', 'fecha_check_out_esperada', 'cantidad_huespedes']
        labels = {
            'fecha_check_in_esperada': 'Check-in',
            'fecha_check_out_esperada': 'Check-out',
            'cantidad_huespedes': 'Huéspedes'
        }
        widgets = {
            'fecha_check_in_esperada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_check_out_esperada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_fecha_check_in_esperada(self):
        fecha_check_in = self.cleaned_data.get('fecha_check_in_esperada')
        if fecha_check_in < timezone.now().date():
            raise ValidationError("La fecha de check-in no puede ser en el pasado.")
        return fecha_check_in

    def clean_fecha_check_out_esperada(self):
        fecha_check_in = self.cleaned_data.get('fecha_check_in_esperada')
        fecha_check_out = self.cleaned_data.get('fecha_check_out_esperada')

        if fecha_check_out and fecha_check_in and fecha_check_out <= fecha_check_in:
            raise ValidationError("La fecha de check-out debe ser posterior a la de check-in.")
        return fecha_check_out

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # Solo si es creación y no edición, valores por defecto para checkin y checkout
            hoy = timezone.now().date()
            maniana = hoy + timezone.timedelta(days=1)
            self.fields['fecha_check_in_esperada'].initial = hoy
            self.fields['fecha_check_out_esperada'].initial = maniana

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        if hasattr(self, 'instance') and self.instance.pk:
            self.helper.form_action = reverse('reserva_editar', args=[self.instance.pk])
        else:
            self.helper.form_action = reverse('reserva_crear')