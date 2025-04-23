from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PeliculaSerializer
from .models import Pelicula

class PeliculaListaAPIView(APIView):
    def get(self, request, format=None):
        categorias = Pelicula.objects.all()
        serializer = PeliculaSerializer(categorias, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = PeliculaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
