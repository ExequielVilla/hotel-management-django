from django import forms
from .models import Habitacion, TipoHabitacion, ServicioHab, FotoHabitacion, CamaTipoHabitacion
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Row, Div
from django.forms import inlineformset_factory
from django.urls import reverse
from django.core.validators import MinValueValidator

class ServicioHabForm(forms.ModelForm):
    class Meta:
        model = ServicioHab
        fields = ['nombre', 'icono']
        widgets = {
            # 'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'icono': forms.HiddenInput()  # Ocultar el campo para que se maneje con JS
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'servicio_habitacion_crear'

    def clean(self):
        super(ServicioHabForm, self).clean()
        nombre = self.cleaned_data.get('nombre')
        icono = self.cleaned_data.get('icono')
        if not icono:
            self._errors['icono'] = self.error_class(['Debe seleccionar un icono'])
        return self.cleaned_data

class TipoCamaForm(forms.Form):
    twin = forms.IntegerField(min_value=0, initial=0, label="Twin")
    double = forms.IntegerField(min_value=0, initial=0, label="Double")
    king = forms.IntegerField(min_value=0, initial=0, label="King")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'  # Estilo horizontal
        self.helper.label_class = 'col-4 pt-1'  # Tamaño y estilo del label
        self.helper.field_class = 'col-8 pe-0'  # Tamaño del input
        self.helper.layout = Layout(
            Row(Field('twin')),
            Row(Field('double')),
            Row(Field('king')),
        )

class TipoHabForm(forms.ModelForm):
    servicios = forms.ModelMultipleChoiceField(
        queryset=ServicioHab.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Servicios",
    )
    precio = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Ej: 1234.56",
        validators=[MinValueValidator(0.01)],
    )
    class Meta:
        model = TipoHabitacion
        fields = ['nombre', 'precio', 'capacidad_maxima', 'servicios']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servicios'].queryset = ServicioHab.objects.filter(activo=True)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        if hasattr(self, 'instance') and self.instance.pk:
            self.helper.form_action = reverse('tipo_habitacion_editar', args=[self.instance.pk])
        else:
            self.helper.form_action = reverse('tipo_habitacion_crear')

class FotoHabForm(forms.ModelForm):
    class Meta:
        model = FotoHabitacion
        fields = ['imagen']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['numero', 'estado', 'tipo_habitacion']
        labels = {
            'numero': 'Nro. de Habitación',
            'tipo_habitacion': 'Tipo de Habitación'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_habitacion'].queryset = TipoHabitacion.objects.filter(activo=True)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        if hasattr(self, 'instance') and self.instance.pk:
            self.helper.form_action = reverse('habitacion_editar', args=[self.instance.pk])
        else:
            self.helper.form_action = reverse('habitacion_crear')

