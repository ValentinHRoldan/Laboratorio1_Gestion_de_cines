from django.db import models
from apps.peliculas.models import Pelicula

class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()
    ubicacion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
class Funcion(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='funciones')
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='funciones')  # ← ESTA ES LA RELACIÓN
    fecha = models.DateField()
    hora = models.TimeField()
    formato = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.pelicula.titulo} - {self.fecha} {self.hora}"
    