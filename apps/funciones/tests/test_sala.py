import pytest
from apps.funciones.models import Sala
from .fixtures_sala import get_sala, get_salas

@pytest.mark.django_db
def test_api_creacion_sala(get_sala):
    print(get_sala)
    assert Sala.objects.filter(ubicacion='Piso 1 - A').exists()

@pytest.mark.django_db
def test_api_creacion_salas(get_salas):
    print(get_salas)
    assert Sala.objects.filter(ubicacion='Piso 1 - A').exists()