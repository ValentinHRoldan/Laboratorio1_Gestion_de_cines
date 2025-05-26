from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ReservaSerializer
from ..models import Reserva
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.exceptions import ValidationError
from apps.funciones.models import Asiento
# class PeliculaListaAPIView(APIView):
#     def get(self, request, format=None):
#         categorias = Reserva.objects.all()
#         serializer = ReservaSerializer(categorias, many=True)
#         return Response(serializer.data)
    
#     def post(self, request, format=None):
#         serializer = ReservaSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservaViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [DjangoModelPermissions] 
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    def perform_create(self, serializer):
        funcion = serializer.validated_data['funcion']
        cantidad = serializer.validated_data['cantidad_entradas']

        # Obtener lista de IDs de asientos desde el request (esperado como lista)
        asiento_ids = self.request.POST.getlist('asientos')
        if not asiento_ids:
            raise ValidationError("Debes seleccionar al menos un asiento.")

        # Validación: función no puede estar en el pasado
        if funcion.fecha < timezone.now().date():
            raise ValidationError("La función ya pasó.")

        # Validar cantidad de entradas coincida con cantidad de asientos
        if len(asiento_ids) != cantidad:
            raise ValidationError("La cantidad de asientos no coincide con la cantidad de entradas.")

        # Obtener objetos Asiento
        asientos = Asiento.objects.filter(id__in=asiento_ids)

        # Validar que existan todos los asientos solicitados
        if asientos.count() != cantidad:
            raise ValidationError("Uno o más asientos no existen.")
        
        sala = funcion.sala
        asientos_validos_en_sala = sala.asientos.filter(id__in=asiento_ids)
        if asientos_validos_en_sala.count() != cantidad:
            raise ValidationError("Uno o más asientos no pertenecen a la sala asignada a esta función.")

        # Verificar si alguno de esos asientos ya está reservado para esa función
        ocupados = Reserva.objects.filter(funcion=funcion, asientos__in=asientos).exists()
        if ocupados:
            raise ValidationError("Uno o más asientos ya están reservados para esta función.")

        # Guardar reserva sin asignar aún los asientos
        reserva = serializer.save()

        # Asociar los asientos a la reserva (ya existe ID)
        reserva.asientos.set(asientos)
        print(reserva.precio_total)