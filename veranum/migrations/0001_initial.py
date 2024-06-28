# Generated by Django 5.0.6 on 2024-06-26 03:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('ubicacion', models.CharField(max_length=200)),
                ('cantidad_habitaciones', models.PositiveIntegerField()),
                ('tipos_habitacion', models.CharField(choices=[('simple', 'Simple'), ('doble', 'Doble'), ('suite', 'Suite')], max_length=50, verbose_name='Categoría')),
            ],
        ),
        migrations.CreateModel(
            name='Habitacion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_habitacion', models.CharField(max_length=100)),
                ('cantidad_personas', models.PositiveIntegerField()),
                ('camas', models.PositiveIntegerField()),
                ('banos', models.PositiveIntegerField()),
                ('precio_por_dia', models.DecimalField(decimal_places=2, max_digits=10)),
                ('disponible', models.BooleanField(default=True)),
                ('descripcion', models.TextField()),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habitaciones', to='veranum.hotel')),
            ],
        ),
    ]