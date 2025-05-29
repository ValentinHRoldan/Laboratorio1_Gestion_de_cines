from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AsientoSerializer, PeliculaSerializer, FuncionSerializer, SalaSerializer, TipoFormatoSerializer
from ..models import Pelicula, Funcion, Sala, TipoFormato, Asiento
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import DjangoModelPermissions
from ..filters import PeliculaFilter
from rest_framework.decorators import action
from apps.reservas.models import AsientoReservado
from gestion_cines.permisos import DjangoModelPermissionsWithView

class PeliculaViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [DjangoModelPermissionsWithView] 

    queryset = Pelicula.objects.all()
    serializer_class = PeliculaSerializer

    #FILTROS
    filterset_class = PeliculaFilter


class FuncionViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [DjangoModelPermissions] 
    filter_backends = [filters.OrderingFilter]

    queryset = Funcion.objects.all()
    serializer_class = FuncionSerializer

    #ORDEN
    ordering_fields = ['fecha', 'hora']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Funcion.objects.all()
        else:
            return Funcion.objects.filter(activa=True)

    @action(detail=True, methods=['get'])
    def disponibilidad(self, request, pk=None):
        funcion = self.get_object()
        serializer = FuncionSerializer(funcion)
        # Todos los asientos
        todos_asientos = funcion.sala.asientos.all()

        # Asientos reservados en esta función
        asientos_reservados = AsientoReservado.objects.filter(funcion=funcion).values_list('asiento_id', flat=True)
        # Asientos que NO están reservados
        asientos_disponibles = todos_asientos.exclude(id__in=asientos_reservados)

        asientos_data = [{'id': asiento.id, 'numero': asiento.numero, 'fila': asiento.fila} for asiento in asientos_disponibles]

        return Response({
            'Funcion': serializer.data,
            'asientos_disponibles': asientos_data
        })

class SalaViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [DjangoModelPermissionsWithView] 
    filter_backends = [filters.OrderingFilter]

    queryset = Sala.objects.all()
    serializer_class = SalaSerializer

    #ORDEN
    ordering_fields = ['capacidad', 'id']


class TipoFormatoViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [DjangoModelPermissionsWithView] 
    queryset = TipoFormato.objects.all()
    serializer_class = TipoFormatoSerializer

class AsientoViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [DjangoModelPermissionsWithView] 
    queryset = Asiento.objects.all()
    serializer_class = AsientoSerializer
