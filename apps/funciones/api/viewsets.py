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


    # def create(self, request, *args, **kwargs):
    #     return Response({'detail': 'No tienes permiso para crear películas.'}, status=403)

    # def update(self, request, *args, **kwargs):
    #     return Response({'detail': 'No tienes permiso para actualizar películas.'}, status=403)

    # def partial_update(self, request, *args, **kwargs):
    #     return Response({'detail': 'No tienes permiso para actualizar parcialmente películas.'}, status=403)

    # def destroy(self, request, *args, **kwargs):
    #     return Response({'detail': 'No tienes permiso para eliminar películas.'}, status=403)


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
        todos_asientos = Asiento.objects.all()

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
    ordering_fields = ['capacidad']


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


#pueden ver las peliculas usuarios autenticados, no autenticados y con cualquier permiso
# class PeliculaViewSet(viewsets.ModelViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticatedOrReadOnly]  # OJO: sólo esta aquí
#     queryset = Pelicula.objects.all()
#     serializer_class = PeliculaSerializer

#     def perform_create(self, serializer):
#         if not self.request.user.has_perm('tuapp.add_pelicula'):
#             # Si no tiene permiso específico para agregar
#             from rest_framework.exceptions import PermissionDenied
#             raise PermissionDenied("No tenés permiso para agregar películas.")
#         serializer.save()

#     def perform_update(self, serializer):
#         if not self.request.user.has_perm('tuapp.change_pelicula'):
#             from rest_framework.exceptions import PermissionDenied
#             raise PermissionDenied("No tenés permiso para editar películas.")
#         serializer.save()

#     def perform_destroy(self, instance):
#         if not self.request.user.has_perm('tuapp.delete_pelicula'):
#             from rest_framework.exceptions import PermissionDenied
#             raise PermissionDenied("No tenés permiso para eliminar películas.")
#         instance.delete()









# class PeliculaListaAPIView(APIView):
#     def get(self, request, format=None):
#         categorias = Pelicula.objects.all()
#         serializer = PeliculaSerializer(categorias, many=True)
#         return Response(serializer.data)
    
#     def post(self, request, format=None):
#         serializer = PeliculaSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)