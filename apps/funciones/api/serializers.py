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
        fields = ['id', 'fila', 'numero', 'sala']

class SalaSerializer(serializers.ModelSerializer):
    asientos = AsientoSerializer(many=True, read_only=True)
    class Meta:
        model = Sala
        fields = ['id','capacidad', 'ubicacion', 'asientos']

class FuncionSerializer(serializers.ModelSerializer):
    pelicula = PeliculaSerializer(read_only=True)
    tipo_formato = TipoFormatoSerializer(read_only=True)
    sala = SalaSerializer(read_only=True)

    pelicula_id = serializers.PrimaryKeyRelatedField(
        queryset=Pelicula.objects.all(), write_only=True
    )
    tipo_formato_id = serializers.PrimaryKeyRelatedField(
        queryset=TipoFormato.objects.all(), write_only=True
    )
    sala_id = serializers.PrimaryKeyRelatedField(
        queryset=Sala.objects.all(), write_only=True
    )

    class Meta:
        model = Funcion
        fields = [
            'id',
            'pelicula', 'pelicula_id',
            'tipo_formato', 'tipo_formato_id',
            'sala', 'sala_id',
            'fecha', 'hora'
        ]

    def generarError(self, mensaje):
        raise serializers.ValidationError({
            'info': mensaje
        })

    def validate_fecha(self, value):
        if value < date.today():
            self.generarError('La fecha no puede ser anterior a la actual')
        return value

    def create(self, validated_data):
        validated_data['pelicula'] = validated_data.pop('pelicula_id')
        validated_data['tipo_formato'] = validated_data.pop('tipo_formato_id')
        validated_data['sala'] = validated_data.pop('sala_id')
        validated_data['activa'] = True  # si es parte del modelo
        return super().create(validated_data)

