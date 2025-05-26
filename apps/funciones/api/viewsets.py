from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AsientoSerializer, PeliculaSerializer, FuncionSerializer, SalaSerializer, TipoFormatoSerializer
from ..models import Pelicula, Funcion, Sala, TipoFormato, Asiento
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import DjangoModelPermissions
from ..filters import PeliculaFilter

class PeliculaViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [DjangoModelPermissions] 

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

class SalaViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [DjangoModelPermissions] 
    filter_backends = [filters.OrderingFilter]

    queryset = Sala.objects.all()
    serializer_class = SalaSerializer

    #ORDEN
    ordering_fields = ['capacidad']


class TipoFormatoViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [DjangoModelPermissions] 
    queryset = TipoFormato.objects.all()
    serializer_class = TipoFormatoSerializer

class AsientoViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [DjangoModelPermissions] 
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