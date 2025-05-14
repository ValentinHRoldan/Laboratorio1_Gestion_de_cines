from django.shortcuts import render
from django.http import JsonResponse
from ..servicios.tmdb import importar_peliculas_estreno

def importar_peliculas_view(request):
    importar_peliculas_estreno()
    return JsonResponse({"mensaje": "Películas importadas correctamente"})
