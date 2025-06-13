import pytest

from apps.reservas.models import AsientoReservado, Reserva
from .fixtures_funcion import get_funcion, get_tipo_formato
from .fixtures_sala import get_sala, get_asiento
from .fixtures_user import create_user, get_user_generico
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def get_reserva(get_user_generico, get_funcion, get_asiento):

    usuario = get_user_generico

    funcion = get_funcion

    reserva, created= Reserva.objects.get_or_create(
        usuario=usuario,
        funcion=funcion,
        defaults={"cantidad_entradas": 1}
    )
    
    if created or not reserva.asientos_reservados.exists():
        AsientoReservado.objects.get_or_create(
            reserva=reserva,
            asiento=get_asiento,
            funcion=funcion
        )

    return reserva

# def create_user(username, documento_identidad, first_name='usuario', last_name='prueba', password='unpassword', email=None, *, is_active=True):
#     email = '{}@root.com'.format(username) if email is None else email

#     user, created = User.objects.get_or_create(username=username, email=email)

#     if created:
#         user.documento_identidad = documento_identidad
#         user.first_name = first_name
#         user.last_name = last_name
#         user.is_active = is_active
#         user.set_password(password)  # Se Hashea la contraseña al guardarla en la BD
#         user.save()

#     return user

# @pytest.fixture
# def get_user_generico_anuncio():
#     test_user = create_user(username='test2', documento_identidad='44326598', first_name='usuario', last_name='last_name', email='test@user.com')
#     return test_user
