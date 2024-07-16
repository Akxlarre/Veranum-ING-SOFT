from django.db import models

class Hotel(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    cantidad_habitaciones = models.PositiveIntegerField()
    tipos_habitacion = models.CharField(max_length=50, choices=[('simple', 'Simple'), ('doble', 'Doble'), ('suite', 'Suite')], verbose_name="Categoría")

    def __str__(self):
        return self.nombre


class Habitacion(models.Model):
    SERVICIOS_EXTRAS_CHOICES = [
        ('Piscina', 'Piscina'),
        ('Gimnasio', 'Gimnasio'),
        ('Spa', 'Spa'),
        ('Canchas de tenis', 'Canchas de tenis')
    ]


    id = models.AutoField(primary_key=True)
    numero_habitacion = models.PositiveIntegerField()
    hotel = models.ForeignKey(Hotel, related_name='habitaciones', on_delete=models.CASCADE)
    tipo_habitacion = models.CharField(max_length=50, choices=[('simple', 'Simple'), ('doble', 'Doble'), ('suite', 'Suite')], verbose_name="Categoría")
    cantidad_personas = models.PositiveIntegerField()
    camas = models.PositiveIntegerField()
    banos = models.PositiveIntegerField()
    precio_por_dia = models.DecimalField(max_digits=10, decimal_places=2)
    historial_precios = models.TextField(blank=True)
    servicios_extras = models.CharField(max_length=255, blank=True)
    disponible = models.BooleanField(default=True)
    descripcion = models.TextField()

    def __str__(self):
        return f'{self.tipo_habitacion} - {self.hotel.nombre}'