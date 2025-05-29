from rest_framework import serializers
from ..models import Pelicula, Funcion, Sala, TipoFormato, Asiento
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from datetime import date, timedelta

class PeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelicula
        fields = ['id', 'titulo', 'duracion', 'genero', 'sinopsis', 'posters', 'clasificacion', 'idioma']


class TipoFormatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoFormato
        fields = ['id','nombre', 'precio']

class AsientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asiento
        fields = ['id', 'fila', 'numero']

class SalaSerializer(serializers.ModelSerializer):
    asientos = AsientoSerializer(many=True, read_only=True)
    class Meta:
        model = Sala
        fields = ['id','capacidad', 'ubicacion', 'asientos']

class FuncionSerializer(serializers.ModelSerializer):
    pelicula = PeliculaSerializer(read_only=True)
    sala = SalaSerializer(read_only=True)
    tipo_formato = TipoFormatoSerializer(read_only=True)
    class Meta:
        model = Funcion
        fields = ['id', 'pelicula', 'sala', 'fecha', 'hora', 'tipo_formato']


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

