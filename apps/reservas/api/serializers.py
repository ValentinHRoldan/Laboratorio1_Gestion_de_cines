from rest_framework import serializers
from ..models import Reserva
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from datetime import timedelta
from apps.funciones.models import Asiento

class ReservaSerializer(serializers.ModelSerializer):
    asientos = serializers.PrimaryKeyRelatedField(queryset=Asiento.objects.all(), many=True)
    class Meta:
        model = Reserva
        fields = ['id', 'usuario', 'funcion', 'cantidad_entradas', 'asientos']

    def generarError(self, mensaje):
        raise serializers.ValidationError({
            'info': mensaje
        })
    
    def validate_cantidad_entradas(self, value):
        if value <= 0:
            self.generarError("Cantidad de entradas minimas: 1")
        return value
    
    
    def validate(self, data):
        if(len(data['asientos']) != data['cantidad_entradas']):
            self.generarError("La cantidad de asientos no coincide con la cantidad de entradas.")
        return data