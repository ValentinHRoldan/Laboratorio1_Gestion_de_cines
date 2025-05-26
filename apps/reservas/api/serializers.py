from rest_framework import serializers

from apps.funciones.api.serializers import AsientoSerializer
from ..models import Reserva
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from datetime import timedelta
from apps.funciones.models import Asiento

class ReservaSerializer(serializers.ModelSerializer):
    # asientos = AsientoSerializer(many=True, read_only=True)
    # asientos_ids = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=Asiento.objects.all(), write_only=True
    # )
    asientos = serializers.PrimaryKeyRelatedField(queryset=Asiento.objects.all(), many=True)
    class Meta:
        model = Reserva
        fields = ['id', 'usuario', 'funcion', 'cantidad_entradas', 'asientos']
