from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import UsuarioSerializer
from rest_framework.response import Response
from ..models import Usuario
from rest_framework import status

@api_view(['POST'])
def register(request):
    serializer = UsuarioSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"user":serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)