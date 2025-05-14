from django.urls import path
from .api.views import importar_peliculas_view

app_name = 'pelicula'
urlpatterns = [
    path("importar-peliculas/", importar_peliculas_view),
]

