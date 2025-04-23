from rest_framework import serializers
from .models import Pelicula
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from datetime import timedelta

class PeliculaSerializer(serializers.ModelSerializer):
    class meta:
        model = Pelicula
        fields = '__all__'