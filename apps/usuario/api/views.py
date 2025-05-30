from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import UsuarioSerializer
from rest_framework.response import Response
from ..models import Usuario
from rest_framework import status
from django.contrib.auth.models import Group

@api_view(['POST'])
def register(request):
    serializer = UsuarioSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        #agregar usuario al grupo creado
        try:
            grupo = Group.objects.get(name="usuarios_registrados")
            user.groups.add(grupo)
        except Group.DoesNotExist:
            return Response({"error": "El grupo 'usuarios_registrados' no existe."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)