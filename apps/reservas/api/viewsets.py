from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ReservaSerializer
from ..models import Reserva


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
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
