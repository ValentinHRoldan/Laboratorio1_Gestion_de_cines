from rest_framework import serializers
from ..models import Pelicula, Funcion, Sala
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from datetime import timedelta

class PeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelicula
        fields = '__all__'

class FuncionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcion
        fields = '__all__'

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = '__all__'