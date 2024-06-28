# urls.py

from django.urls import path
from .views import editar_habitacion, editar_hotel, get_habitacion_info, get_hotel_info, lista_hoteles, lista_habitaciones, eliminar_hotel, eliminar_habitacion

urlpatterns = [
    path('', lista_hoteles, name='lista_hoteles'),
    path('habitaciones/<int:hotel_id>/', lista_habitaciones, name='lista_habitaciones'),
    path('habitaciones/editar/<int:habitacion_id>/', editar_habitacion, name='editar_habitacion'),
    path('habitaciones/eliminar/<int:habitacion_id>/', eliminar_habitacion, name='eliminar_habitacion'),
    path('get_habitacion_info/<int:habitacion_id>/', get_habitacion_info, name='get_habitacion_info'),
    path('get_hotel_info/<int:hotel_id>/', get_hotel_info, name='get_hotel_info'),
    path('editar_hotel/<int:hotel_id>/', editar_hotel, name='editar_hotel'),  
    path('eliminar_hotel/<int:hotel_id>/', eliminar_hotel, name='eliminar_hotel'),
    path('eliminar_habitacion/<int:habitacion_id>/', eliminar_habitacion, name='eliminar_habitacion'),
]
