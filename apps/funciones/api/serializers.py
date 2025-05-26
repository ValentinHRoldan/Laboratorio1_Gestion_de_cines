from rest_framework import serializers
from ..models import Pelicula, Funcion, Sala, TipoFormato, Asiento
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from datetime import date, timedelta

class PeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelicula
        fields = '__all__'


class FuncionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcion
        fields = ['id', 'pelicula', 'sala', 'fecha', 'hora', 'tipo_formato', 'activa']


    def generarError(self, mensaje):
        raise serializers.ValidationError({
            'info': mensaje
        })

    def validate_fecha(self, value):
        if value < date.today():
            self.generarError('la fecha no puede ser anterior a la actual')
        return value

    def create(self, validated_data):
        validated_data['activa'] = True
        return super().create(validated_data)

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = '__all__'

class TipoFormatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoFormato
        fields = '__all__'

class AsientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asiento
        fields = '__all__'