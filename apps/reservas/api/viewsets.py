from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ReservaSerializer
from ..models import Reserva
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.exceptions import ValidationError
from apps.funciones.models import Asiento
from apps.reservas.models import AsientoReservado
from gestion_cines.permisos import DjangoModelPermissionsWithView

class ReservaViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [DjangoModelPermissions]
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Reserva.objects.all()
        else:
            return Reserva.objects.filter(usuario_id=user.id)
        
    def list(self, request, *args, **kwargs):
        print("Permisos activos del usuario:", request.user.get_all_permissions())
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        usuario = self.request.user
        funcion = serializer.validated_data['funcion_id']
        asiento_ids = self.request.data.get('asientos', [])
        # desde el postman se envía una lista de IDs

        asientos = Asiento.objects.filter(id__in=asiento_ids)

        #validar los asientos que pertenecen a la sala de la función
        for asiento in asientos:
            if asiento.sala != funcion.sala:
                raise ValidationError(
                    f"El asiento {asiento.fila}{asiento.numero} no pertenece a la sala de la función."
                )

        #se verifica si los asientos ya estan reservados para esta funcion
        for asiento in asientos:
            if AsientoReservado.objects.filter(asiento=asiento, funcion=funcion).exists():
                raise ValidationError(
                    f"El asiento {asiento.fila}{asiento.numero} ya está reservado para esta función."
                )

        #se guarda la reserva
        reserva = serializer.save(usuario=usuario)

        # Crear las instancias de AsientoReservado
        for asiento in asientos:
            AsientoReservado.objects.create(
                reserva=reserva,
                asiento=asiento,
                funcion=funcion
            )

        print("PRECIO TOTAL DE RESERVA:", reserva.precio_total)