import pytest
from apps.funciones.models import Asiento
from .fixtures_sala import get_asiento, get_asientos, get_sala

@pytest.mark.django_db
def test_api_creacion_asiento(get_asiento):
    print(get_asiento)
    assert Asiento.objects.filter(fila='C').exists()

@pytest.mark.django_db
def test_api_creacion_asientos(get_asientos):
    print(get_asientos)
    assert Asiento.objects.filter(fila='C').exists()