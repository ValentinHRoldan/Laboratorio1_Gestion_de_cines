from rest_framework import serializers
from ..models import Reserva
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from datetime import timedelta
from apps.funciones.models import Asiento

class ReservaSerializer(serializers.ModelSerializer):
    asientos = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Asiento.objects.all()
    )
    class Meta:
        model = Reserva
        fields = '__all__'
