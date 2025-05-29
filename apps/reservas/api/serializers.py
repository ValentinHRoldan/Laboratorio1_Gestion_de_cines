from rest_framework import serializers
from ..models import Reserva, AsientoReservado
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from datetime import timedelta
from apps.funciones.models import Asiento, Funcion
from apps.funciones.api.serializers import AsientoSerializer, FuncionSerializer
from apps.usuario.api.serializers import UsuarioSerializer

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
    funcion = FuncionSerializer(read_only = True)
    funcion_id = serializers.PrimaryKeyRelatedField(
        queryset=Funcion.objects.all(), write_only=True  # Para POST
    )
    usuario = UsuarioSerializer(read_only = True)
    class Meta:
        model = Reserva
        fields = ['id', 'usuario', 'funcion', 'funcion_id', 'cantidad_entradas', 'asientos', 'asientos_reservados', 'precio_total']
        read_only_fields = ['usuario', 'asientos_reservados', 'precio_total']

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
        funcion = validated_data.pop('funcion_id')
        validated_data['funcion'] = funcion
        #sacamos los asientos 
        asiento_ids = validated_data.pop('asientos')  
        
        #se crea la reserva sin los asientos
        reserva = Reserva.objects.create(**validated_data)

        #se los devuelve al perform_create para que los procese
        self.context['asiento_ids'] = asiento_ids
        return reserva
    
