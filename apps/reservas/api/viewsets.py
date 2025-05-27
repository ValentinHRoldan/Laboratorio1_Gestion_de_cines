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
        asiento_ids = self.request.POST.getlist('asientos')

        asientos = Asiento.objects.filter(id__in=asiento_ids)
        print(asientos,len(asientos),type(len(asientos)),asiento_ids)
        for asiento in asientos:
            if asiento.sala != funcion.sala:
                raise ValidationError(f"El asiento {asiento.fila}{asiento.numero} no pertenece a la sala de la función.")

        # Verificar si ya están reservados
        ocupados = Reserva.objects.filter(funcion=funcion, asientos__in=asientos).exists()
        if ocupados:
            raise ValidationError("Uno o más asientos ya están reservados para esta función.")

        # Paso crítico: guardar la reserva SIN los asientos aún
        reserva = serializer.save()

        # Ahora sí, ya tiene ID → podemos asignar asientos
        reserva.asientos.set(asientos)
        print("PRECIO TOTAL DE RESERVA:", reserva.precio_total)