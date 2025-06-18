import pytest
from apps.funciones.models import Pelicula
from .fixtures_funcion import get_pelicula

@pytest.mark.django_db
def test_api_creacion_pelicula(get_pelicula):
    print(get_pelicula)
    assert Pelicula.objects.filter(titulo='Inception').exists()