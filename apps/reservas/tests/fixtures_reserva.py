import pytest

from apps.reservas.models import AsientoReservado, Reserva
from .fixtures_funcion import get_funcion, get_tipo_formato, get_funciones
from .fixtures_sala import get_sala, get_asiento, get_asientos
from .fixtures_user import get_user_generico, get_super_user
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def get_reserva(get_user_generico, get_funcion, get_asientos):

    usuario = get_user_generico

    funcion = get_funcion

    reserva, created= Reserva.objects.get_or_create(
        usuario=usuario,
        funcion=funcion,
        defaults={"cantidad_entradas": 3}
    )
    
    if created or not reserva.asientos_reservados.exists():
        for asiento in get_asientos:
            AsientoReservado.objects.get_or_create(
                reserva=reserva,
                asiento=asiento,
                funcion=funcion
            )

    return reserva

@pytest.fixture #devuelve 3 reservas, 2 creadas por un usuario GENERICO y 1 por un usuario ADMIN
def get_reservas(get_user_generico, get_super_user, get_funciones, get_asientos):

    usuario1 = get_user_generico
    usuario2 = get_super_user

    funcion1, funcion2, funcion3 = get_funciones
    asiento1, asiento2, asiento3 = get_asientos

    #RESERVA1

    reserva1, created= Reserva.objects.get_or_create(
        usuario=usuario1,
        funcion=funcion1,
        defaults={"cantidad_entradas": 1}
    )
    
    if created or not reserva1.asientos_reservados.exists():
        AsientoReservado.objects.get_or_create(
            reserva=reserva1,
            asiento=asiento1,
            funcion=funcion1
        )

    #RESERVA2

    reserva2, created= Reserva.objects.get_or_create(
        usuario=usuario2,
        funcion=funcion2,
        defaults={"cantidad_entradas": 1}
    )
    
    if created or not reserva2.asientos_reservados.exists():
        AsientoReservado.objects.get_or_create(
            reserva=reserva2,
            asiento=asiento2,
            funcion=funcion2
        )

    #RESERVA3

    reserva3, created= Reserva.objects.get_or_create(
        usuario=usuario1,
        funcion=funcion3,
        defaults={"cantidad_entradas": 1}
    )
    
    if created or not reserva3.asientos_reservados.exists():
        AsientoReservado.objects.get_or_create(
            reserva=reserva3,
            asiento=asiento3,
            funcion=funcion3
        )

    return reserva1, reserva2, reserva3
