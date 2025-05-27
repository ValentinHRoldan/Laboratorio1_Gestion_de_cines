# Create your models here.
from django.db import models
from apps.usuario.models import Usuario
from apps.funciones.models import Funcion, Asiento
from django.core.exceptions import ValidationError

class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reservas_usuario')
    funcion = models.ForeignKey(Funcion, on_delete=models.CASCADE, related_name='reservas_funcion')
    cantidad_entradas = models.PositiveIntegerField()

    def __str__(self):
        return f"Reserva de {self.usuario.username} para {self.funcion}"
    
    @property
    def precio_total(self):
        return self.cantidad_entradas * self.funcion.tipo_formato.precio
    

class AsientoReservado(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='asientos_reservados')
    asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE)
    funcion = models.ForeignKey(Funcion, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('asiento', 'funcion')  # asegura que un asiento no se reserve dos veces en la misma función