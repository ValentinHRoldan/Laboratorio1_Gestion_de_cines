import pytest
from apps.usuario.models import Usuario
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.funciones.models import Funcion
from apps.reservas.models import Reserva, AsientoReservado

@pytest.fixture
def test_password():
    return "secure_password_123"

@pytest.fixture
def grupo_usuarios_registrados():
    group, created = Group.objects.get_or_create(name="usuarios_registrados")

    # Permisos para el modelo Funcion
    content_type_funcion = ContentType.objects.get_for_model(Funcion)
    permisos_funcion = Permission.objects.filter(
        content_type=content_type_funcion,
        codename='view_funcion',
    )

    # Permisos para el modelo AsientoReservado
    content_type_asiento = ContentType.objects.get_for_model(AsientoReservado)
    permisos_asiento = Permission.objects.filter(
        content_type=content_type_asiento,
        codename__in=[
            'view_asientoreservado',
            'add_asientoreservado',
            'change_asientoreservado',
            'delete_asientoreservado',
        ]
    )

    # Permisos para el modelo Reserva
    content_type_reserva = ContentType.objects.get_for_model(Reserva)
    permisos_reserva = Permission.objects.filter(
        content_type=content_type_reserva,
        codename__in=[
            'add_reserva',
            'change_reserva',
            'delete_reserva',
        ]
    )

    # Asignar todos los permisos al grupo
    group.permissions.set(
        list(permisos_funcion) + list(permisos_asiento) + list(permisos_reserva)
    )

    return group


@pytest.fixture
def create_user(test_password, grupo_usuarios_registrados):
    User = get_user_model()
    user = User.objects.create_user(
        username="testuser",
        nombre="nombretest",
        apellido="apellidotest",
        password=test_password,
        documento="12345678",
        email="email@test.com",
    )
    user.groups.add(grupo_usuarios_registrados)
    return user


@pytest.fixture
def create_superuser(test_password):
    User = get_user_model()
    user = User.objects.create_user(
        username="testsuperuser",
        password=test_password,
        documento_identidad="87654321",
        domicilio="Calle Falsa 123",
        email="testsup@example.com",
        is_superuser = True
    )
    return user