import pytest
from apps.funciones.models import TipoFormato
from .fixtures_funcion import get_tipo_formato, get_tipos_formatos

# Test unitario: Prueba la creación de un formato
@pytest.mark.django_db
def test_api_creacion_formato(get_tipo_formato):
    print(get_tipo_formato)
    assert TipoFormato.objects.filter(nombre='2D').exists()

# Test unitario: Prueba la creación de múltiples formatos
@pytest.mark.django_db
def test_api_creacion_formatos(get_tipos_formatos):
    print(get_tipos_formatos)
    assert TipoFormato.objects.filter(nombre='2D').exists()