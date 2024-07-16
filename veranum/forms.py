from django import forms
from .models import Hotel, Habitacion

class RegistrarHotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['nombre', 'ubicacion', 'cantidad_habitaciones',]

class RegistrarHabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = '__all__'
        exclude = ['historial_precios']

    servicios_extras = forms.MultipleChoiceField(
        choices=Habitacion.SERVICIOS_EXTRAS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def clean_servicios_extras(self):
        data = self.cleaned_data['servicios_extras']
        return ','.join(data)

class EditarHabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = '__all__'
        exclude = ['hotel', 'historial_precios']

    servicios_extras = forms.MultipleChoiceField(
        choices=Habitacion.SERVICIOS_EXTRAS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(EditarHabitacionForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['servicios_extras'] = self.instance.servicios_extras.split(',')

    def clean_servicios_extras(self):
        data = self.cleaned_data['servicios_extras']
        return ','.join(data)  # Convertir de lista a cadena separada por comas
    
class EditarHotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['nombre', 'ubicacion', 'cantidad_habitaciones',]
