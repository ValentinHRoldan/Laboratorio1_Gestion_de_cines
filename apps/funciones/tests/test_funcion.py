import pytest
from apps.funciones.models import Funcion
from .fixtures_funcion import get_funcion, get_pelicula, get_tipo_formato
from .fixtures_sala import get_sala

@pytest.mark.django_db
def test_api_creacion_funcion(get_funcion):
    print(get_funcion)
    assert Funcion.objects.filter(sala=1).exists()