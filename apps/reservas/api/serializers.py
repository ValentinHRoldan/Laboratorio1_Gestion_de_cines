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
