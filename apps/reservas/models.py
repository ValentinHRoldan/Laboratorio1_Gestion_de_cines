# Create your models here.
from django.db import models
from apps.usuario.models import Usuario
from apps.funciones.models import Funcion

class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reservas_usuario')
    funcion = models.ForeignKey(Funcion, on_delete=models.CASCADE, related_name='reservas_funcion')
    cantidad_entradas = models.PositiveIntegerField()
    asiento = models.CharField(max_length=10)

    class Meta:
        unique_together = ('funcion', 'asiento') #evita duplicaciones de asiento / funcion

    def __str__(self):
        return f"Reserva de {self.usuario.nombre} para {self.funcion}"
    
    @property
    def precio_total(self):
        return self.cantidad_entradas * self.funcion.precio_unitario