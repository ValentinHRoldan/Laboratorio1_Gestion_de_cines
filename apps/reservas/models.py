# Create your models here.
from django.db import models
from apps.usuarios.models import Usuario
from apps.funciones.models import Funcion

class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reservas_usuario')
    funcion = models.ForeignKey(Funcion, on_delete=models.CASCADE, related_name='reservas_funcion')
    cantidad_entradas = models.PositiveIntegerField()
    asiento = models.CharField(max_length=10)
    precio_total = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Reserva de {self.usuario.nombre} para {self.funcion}"