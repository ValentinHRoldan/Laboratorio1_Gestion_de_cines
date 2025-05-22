# Create your models here.
from django.db import models
from apps.usuario.models import Usuario
from apps.funciones.models import Funcion, Asiento
from django.core.exceptions import ValidationError

class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reservas_usuario')
    funcion = models.ForeignKey(Funcion, on_delete=models.CASCADE, related_name='reservas_funcion')
    cantidad_entradas = models.PositiveIntegerField()
    asientos = models.ManyToManyField(Asiento, related_name='reservas_asiento')

    def __str__(self):
        return f"Reserva de {self.usuario.username} para {self.funcion}"
    
    @property
    def precio_total(self):
        return self.cantidad_entradas * self.funcion.precio_unitario

    def clean(self):
        # Verificar que ningún asiento esté ya reservado para la misma función
        if self.pk is None:
            # La reserva aún no fue guardada
            asientos_conflictivos = Reserva.objects.filter(
                funcion=self.funcion,
                asientos__in=self.asientos.all()
            ).exists()
        else:
            # Si la reserva ya existe (edición), excluirla de la búsqueda
            asientos_conflictivos = Reserva.objects.exclude(
                pk=self.pk
            ).filter(
                funcion=self.funcion,
                asientos__in=self.asientos.all()
            ).exists()

        if asientos_conflictivos:
            raise ValidationError("Uno o más asientos ya han sido reservados para esta función.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Llama a clean() antes de guardar
        super().save(*args, **kwargs)