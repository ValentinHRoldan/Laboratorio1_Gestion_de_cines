import pytest

from apps.funciones.models import Sala, Asiento

@pytest.fixture
def get_sala():
    sala, _ = Sala.objects.get_or_create(
        ubicacion="Piso 1 - A",
    )
    return sala

@pytest.fixture
def get_salas():
    sala1, _ = Sala.objects.get_or_create(
        ubicacion="Piso 1 - A",
    )

    sala2, _ = Sala.objects.get_or_create(
        ubicacion="Piso 1 - B",
    )

    sala3, _ = Sala.objects.get_or_create(
        ubicacion="Piso 2 - A",
    )
    return sala1, sala2, sala3

@pytest.fixture
def get_asiento(get_sala):
    asiento, _ = Asiento.objects.get_or_create(
        defaults={
            "sala": get_sala,
            "fila": "C",
            "numero": 2
        }
    )

    return asiento

@pytest.fixture
def get_asientos(get_sala):
    asiento1, _ = Asiento.objects.get_or_create(
        defaults={
            "sala": get_sala,
            "fila": "C",
            "numero": 1
        }
    )

    asiento2, _ = Asiento.objects.get_or_create(
        defaults={
            "sala": get_sala,
            "fila": "B",
            "numero": 2
        }
    )

    asiento3, _ = Asiento.objects.get_or_create(
        defaults={
            "sala": get_sala,
            "fila": "A",
            "numero": 3
        }
    )

    return asiento1, asiento2, asiento3