# views.py

from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import EditarHabitacionForm, EditarHotelForm, RegistrarHotelForm, RegistrarHabitacionForm
from .models import Hotel, Habitacion
from django.views.decorators.http import require_POST


def index(request):
    return render(request, 'veranum/index.html')

def lista_hoteles(request, tipo_usuario):
    hoteles = Hotel.objects.all()
    formRegistro = RegistrarHotelForm()
    formEdicion = None  # Formulario de edición inicialmente vacío

    if request.method == 'POST':
        if 'registrar' in request.POST:
            formRegistro = RegistrarHotelForm(request.POST)
            if formRegistro.is_valid():
                formRegistro.save()
                return redirect('lista_hoteles', tipo_usuario)
        elif 'editar' in request.POST:
            hotel_id = request.POST.get('hotel_id')
            hotel = get_object_or_404(Hotel, pk=hotel_id)
            formEdicion = EditarHotelForm(instance=hotel)  # Llenar formulario con datos del hotel
            if request.method == 'POST':
                formEdicion = EditarHotelForm(request.POST, instance=hotel)
                if formEdicion.is_valid():
                    formEdicion.save()
                    return redirect('lista_hoteles', tipo_usuario)

    context = {
        'tipo_usuario': tipo_usuario,
        'hoteles': hoteles,
        'formRegistro': formRegistro,
        'formEdicion': formEdicion,
    }

    return render(request, 'veranum/hoteles.html', context)

def get_hotel_info(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    habitaciones = hotel.habitaciones.all()
    data = {
        'nombre': hotel.nombre,
        'cantidad_habitaciones': hotel.cantidad_habitaciones,
        'ubicacion': hotel.ubicacion,
        'tipos_habitacion': hotel.tipos_habitacion,
        'habitaciones': list(habitaciones.values()),
    }
    return JsonResponse(data)


def eliminar_hotel(request, hotel_id, tipo_usuario):

    hotel = get_object_or_404(Hotel, pk=hotel_id)
    hotel.delete()
    return redirect('lista_hoteles', tipo_usuario)

def eliminar_habitacion(request, habitacion_id , tipo_usuario):
    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)
    hotel_id = habitacion.hotel.id
    habitacion.delete()
    return redirect('lista_habitaciones', hotel_id=hotel_id , tipo_usuario=tipo_usuario)
def editar_hotel(request, hotel_id , tipo_usuario):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    if request.method == 'POST':
        form = EditarHotelForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect('lista_hoteles', tipo_usuario )  # Redirigir a la lista de hoteles después de editar
    else:
        form = EditarHotelForm(instance=hotel)
    
    context = {
        'tipo_usuario' : tipo_usuario,
        'form': form,
        'hotel': hotel,
    }
    return render(request, 'veranum/editar_hotel.html', context)


def lista_habitaciones(request, hotel_id , tipo_usuario):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    habitaciones = hotel.habitaciones.all()
    form = RegistrarHabitacionForm()

    if request.method == 'POST':
        form = RegistrarHabitacionForm(request.POST)
        if form.is_valid():
            habitacion = form.save(commit=False)
            fecha_actual = datetime.now()
            # Convertir la fecha a string en el formato deseado (por ejemplo, 'YYYY-MM-DD')
            fecha_como_cadena = fecha_actual.strftime('%Y-%m-%d')
            habitacion.historial_precios += f"; {habitacion.precio_por_dia} - {fecha_como_cadena}"
            habitacion.hotel = hotel
            habitacion.save()
            return redirect('lista_habitaciones', hotel_id=hotel_id , tipo_usuario=tipo_usuario)


    context = {
        'tipo_usuario' : tipo_usuario,
        'form': RegistrarHabitacionForm(),  
        'hotel': hotel,
        'habitaciones': habitaciones,
    }
    return render(request, 'veranum/lista_habitaciones.html', context)


def editar_habitacion(request, habitacion_id , tipo_usuario):
    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)
    hotel = habitacion.hotel

    if request.method == 'POST':
        form = EditarHabitacionForm(request.POST, instance=habitacion)
        if form.is_valid():
            habitacion = form.save(commit=False)
            precio_por_dia_str = str(habitacion.precio_por_dia)
            fecha_actual_str = datetime.now().strftime('%Y-%m-%d')
            precio_y_fecha = f"{precio_por_dia_str} - {fecha_actual_str}"

            if precio_y_fecha not in habitacion.historial_precios:
                if habitacion.historial_precios:
                    historial_list = habitacion.historial_precios.split(',')
                    historial_list.append(precio_y_fecha)
                    habitacion.historial_precios = ','.join(historial_list)
                else:
                    habitacion.historial_precios = precio_y_fecha
            habitacion.save()
            return redirect('lista_habitaciones', hotel_id=habitacion.hotel.id, tipo_usuario=tipo_usuario)
    else:
        form = EditarHabitacionForm(instance=habitacion)

    context = {
        'tipo_usuario' : tipo_usuario,
        'hotel': hotel,
        'form': form,
        'habitacion': habitacion,
    }
    return render(request, 'veranum/editar_habitacion.html', context)

def eliminar_habitacion(request, habitacion_id , tipo_usuario):
    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)
    hotel_id = habitacion.hotel.id
    habitacion.delete()
    return redirect('lista_habitaciones', hotel_id=hotel_id , tipo_usuario=tipo_usuario)


@require_POST
def cambiar_disponibilidad(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)
    habitacion.disponible = not habitacion.disponible
    habitacion.save()
    return JsonResponse({'status': 'success', 'disponible': habitacion.disponible})

def get_habitacion_info(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)
    data = {
        'tipo_habitacion': habitacion.tipo_habitacion,
        'cantidad_personas': habitacion.cantidad_personas,
        'camas': habitacion.camas,
        'banos': habitacion.banos,
        'precio_por_dia': str(habitacion.precio_por_dia),
        'disponible': habitacion.disponible,
        'historial_precios': habitacion.historial_precios,
        'servicios_extras': habitacion.servicios_extras,
        'descripcion': habitacion.descripcion,
    }
    return JsonResponse(data)