import pytest

from apps.funciones.models import Funcion, Pelicula, TipoFormato
from .fixtures_sala import get_sala

@pytest.fixture
def get_funcion(get_sala, get_pelicula, get_tipo_formato):
    funcion, _ = Funcion.objects.get_or_create(
        defaults={
            "pelicula": get_pelicula,
            "sala": get_sala,
            "fecha": "2025-06-15",
            "hora": "18:00:00",
            "tipo_formato": get_tipo_formato,
        }
    )

    return funcion

@pytest.fixture
def get_pelicula():
    pelicula, _ = Pelicula.objects.get_or_create(
        titulo='Inception',
        defaults={
            "duracion": 148,
            "genero": "Sci-Fi",
            "sinopsis": "Un ladrón especializado en robar secretos mediante el uso de la tecnología de sueños compartidos recibe una oferta para implantar una idea en la mente de un objetivo.",
            "posters": "https://example.com/poster/inception.jpg",
            "clasificacion": "PG-13",
            "idioma": "Inglés",
            "trailer": "https://example.com/trailer/inception.mp4"
        }
    )

    return pelicula


@pytest.fixture
def get_tipo_formato():
    tipo_formato, _ = TipoFormato.objects.get_or_create(
        nombre='2D',
        defaults={
            "precio": 6000
        }
    )

    return tipo_formato

@pytest.fixture
def get_tipos_formatos():

    tipo_formato1, _ = TipoFormato.objects.get_or_create(
        nombre='2D',
        defaults={
            "precio": 6000
        }
    )

    tipo_formato2, _ = TipoFormato.objects.get_or_create(
        nombre='3D',
        defaults={
            "precio": 8000
        }
    )

    tipo_formato3, _ = TipoFormato.objects.get_or_create(
        nombre='IMAX',
        defaults={
            "precio": 10000
        }
    )

    return tipo_formato1, tipo_formato2, tipo_formato3