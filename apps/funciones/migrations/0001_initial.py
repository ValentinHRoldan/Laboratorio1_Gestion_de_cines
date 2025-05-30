# Generated by Django 5.1.7 on 2025-04-23 22:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pelicula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('duracion', models.PositiveIntegerField()),
                ('genero', models.CharField(max_length=100)),
                ('sinopsis', models.TextField()),
                ('posters', models.URLField()),
                ('clasificacion', models.CharField(max_length=50)),
                ('idioma', models.CharField(max_length=50)),
                ('trailer', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('capacidad', models.PositiveIntegerField()),
                ('ubicacion', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Funcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('formato', models.CharField(max_length=50)),
                ('pelicula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funciones', to='funciones.pelicula')),
                ('sala', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funciones', to='funciones.sala')),
            ],
        ),
    ]
