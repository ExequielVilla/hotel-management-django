from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Huesped
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import inlineformset_factory
from django.urls import reverse
from django.core.validators import MinValueValidator


# class CustomLoginForm(AuthenticationForm):
#     username = forms.CharField(
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su usuario'}),
#         label=''  # Oculta la etiqueta
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'}),
#         label=''  # Oculta la etiqueta
#     )

class HuespedForm(forms.ModelForm):
    class Meta:
        model = Huesped
        fields = ['nombre', 'apellido', 'dni_pasaporte', 'email', 'telefono', 'preferencias']
        labels = {
            'dni_pasaporte': 'DNI/Pasaporte',
            'telefono': 'Teléfono'
        }
        widgets = {
            'preferencias': forms.Textarea(attrs={
                'rows': 3,  # Altura en líneas
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        if hasattr(self, 'instance') and self.instance.pk:
            self.helper.form_action = reverse('huesped_editar', args=[self.instance.pk])
        else:
            self.helper.form_action = reverse('huesped_crear')