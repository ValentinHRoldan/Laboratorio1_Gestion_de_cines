from rest_framework import serializers
from ..models import Reserva, AsientoReservado
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from datetime import timedelta
from apps.funciones.models import Asiento
from apps.funciones.api.serializers import AsientoSerializer

class AsientoReservadoSerializer(serializers.ModelSerializer):
    asiento = AsientoSerializer(read_only=True)
    class Meta:
        model = AsientoReservado
        fields = ['id', 'asiento', 'funcion']

class ReservaSerializer(serializers.ModelSerializer):
    asientos = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    asientos_reservados = AsientoReservadoSerializer(many=True, read_only=True)
    class Meta:
        model = Reserva
        fields = ['id', 'usuario', 'funcion', 'cantidad_entradas', 'asientos', 'asientos_reservados']
        read_only_fields = ['usuario', 'asientos_reservados']

    def generarError(self, mensaje):
        raise serializers.ValidationError({
            'info': mensaje
        })
    
    def validate_cantidad_entradas(self, value):
        if value <= 0:
            self.generarError("Cantidad de entradas minimas: 1")
        return value
    
    def validate_funcion(self, value):
        if value.fecha < timezone.now().date():
            self.generarError("La función ya pasó.")
        return value

    def validate(self, data):
        if(len(data['asientos']) != data['cantidad_entradas']):
            self.generarError("La cantidad de asientos no coincide con la cantidad de entradas.")
        return data
    
    def create(self, validated_data):
        asiento_ids = validated_data.pop('asientos')  # Sacamos los asientos
        
        # Creamos la reserva sin los asientos
        reserva = Reserva.objects.create(**validated_data)

        # Los devolvemos para que perform_create los procese
        self.context['asiento_ids'] = asiento_ids
        return reserva
    
