# views.py

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import EditarHabitacionForm, EditarHotelForm, RegistrarHotelForm, RegistrarHabitacionForm
from .models import Hotel, Habitacion

def lista_hoteles(request):
    hoteles = Hotel.objects.all()
    formRegistro = RegistrarHotelForm()
    formEdicion = None  # Formulario de edición inicialmente vacío

    if request.method == 'POST':
        if 'registrar' in request.POST:
            formRegistro = RegistrarHotelForm(request.POST)
            if formRegistro.is_valid():
                formRegistro.save()
                return redirect('lista_hoteles')
        elif 'editar' in request.POST:
            hotel_id = request.POST.get('hotel_id')
            hotel = get_object_or_404(Hotel, pk=hotel_id)
            formEdicion = EditarHotelForm(instance=hotel)  # Llenar formulario con datos del hotel
            if request.method == 'POST':
                formEdicion = EditarHotelForm(request.POST, instance=hotel)
                if formEdicion.is_valid():
                    formEdicion.save()
                    return redirect('lista_hoteles')

    context = {
        'hoteles': hoteles,
        'formRegistro': formRegistro,
        'formEdicion': formEdicion,
    }

    return render(request, 'veranum/hoteles.html', context)

def get_hotel_info(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    data = {
        'nombre': hotel.nombre,
        'cantidad_habitaciones': hotel.cantidad_habitaciones,
        'ubicacion': hotel.ubicacion,
        'tipos_habitacion': hotel.tipos_habitacion
    }
    return JsonResponse(data)


def eliminar_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    hotel.delete()
    return redirect('lista_hoteles')

def eliminar_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)
    hotel_id = habitacion.hotel.id
    habitacion.delete()
    return redirect('lista_habitaciones', hotel_id=hotel_id)

def editar_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    if request.method == 'POST':
        form = EditarHotelForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect('lista_hoteles')  # Redirigir a la lista de hoteles después de editar
    else:
        form = EditarHotelForm(instance=hotel)
    
    context = {
        'form': form,
        'hotel': hotel,
    }
    return render(request, 'veranum/editar_hotel.html', context)


def lista_habitaciones(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    habitaciones = hotel.habitaciones.all()
    form = RegistrarHabitacionForm()

    if request.method == 'POST':
        form = RegistrarHabitacionForm(request.POST)
        if form.is_valid():
            habitacion = form.save(commit=False)
            habitacion.hotel = hotel
            habitacion.save()
            return redirect('lista_habitaciones', hotel_id=hotel_id)


    context = {
        'form': RegistrarHabitacionForm(),  
        'hotel': hotel,
        'habitaciones': habitaciones,
    }
    return render(request, 'veranum/lista_habitaciones.html', context)


def editar_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)
    hotel = habitacion.hotel

    if request.method == 'POST':
        form = EditarHabitacionForm(request.POST, instance=habitacion)
        if form.is_valid():
            form.save()
            return redirect('lista_habitaciones', hotel_id=hotel.id)
    else:
        form = EditarHabitacionForm(instance=habitacion)

    context = {
        'hotel': hotel,
        'form': form,
        'habitacion': habitacion,
    }
    return render(request, 'veranum/editar_habitacion.html', context)

def eliminar_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)
    hotel_id = habitacion.hotel.id
    habitacion.delete()
    return redirect('lista_habitaciones', hotel_id=hotel_id)

def get_habitacion_info(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)
    data = {
        'tipo_habitacion': habitacion.tipo_habitacion,
        'cantidad_personas': habitacion.cantidad_personas,
        'camas': habitacion.camas,
        'banos': habitacion.banos,
        'precio_por_dia': str(habitacion.precio_por_dia),
        'disponible': habitacion.disponible,
        'descripcion': habitacion.descripcion,
    }
    return JsonResponse(data)