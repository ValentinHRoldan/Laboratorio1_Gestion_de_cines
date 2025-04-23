from rest_framework import serializers
from .models import Reserva
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from datetime import timedelta

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'
