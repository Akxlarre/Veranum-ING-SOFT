from django import forms
from .models import Hotel, Habitacion

class RegistrarHotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'

class RegistrarHabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = '__all__'
        exclude = ['hotel']

class EditarHabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = '__all__'
        exclude = ['hotel']


class EditarHotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['nombre', 'ubicacion', 'cantidad_habitaciones', 'tipos_habitacion']
