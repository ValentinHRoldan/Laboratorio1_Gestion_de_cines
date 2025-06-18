import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework.authtoken.models import Token
from django.contrib.contenttypes.models import ContentType
from rest_framework_simplejwt.tokens import RefreshToken

from apps.funciones.models import Funcion
from apps.reservas.models import AsientoReservado, Reserva
from apps.usuario.models import Usuario

User = get_user_model()


# def create_user(username, documento_identidad, first_name='Micaela', last_name='Salgado', password='unpassword', email=None, *, is_active=True):
#     email = '{}@root.com'.format(username) if email is None else email

#     user, created = User.objects.get_or_create(username=username, email=email)

#     if created:
#         user.documento_identidad = documento_identidad
#         user.first_name = first_name
#         user.last_name = last_name
#         user.is_active = is_active
#         user.set_password(password)  # Se Hashea la contraseña al guardarla en la BD
#         user.save()

#         #creación de grupo "usuarios_registrados"
#         grupo, _ = Group.objects.get_or_create(name='usuarios_registrados')

#         permisos_deseados = ['add_reserva', 'change_reserva', 'delete_reserva','add_asiento_reservado'
#                                 , 'change_asiento_reservado', 'delete_asiento_reservado', 'view_asiento_reservado'
#                                 , 'view_funcion']
#         for codename in permisos_deseados:
#             permiso = Permission.objects.get(codename=codename)
#             grupo.permissions.add(permiso)

#         user.groups.add(grupo)

#     return user

@pytest.fixture
def get_user_generico(test_password, grupo_usuarios_registrados):

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
def get_super_user(test_password):
    User = get_user_model()
    user = User.objects.create_user(
        username="testsuperuser",
        nombre="nombretestsuper",
        apellido="apellidotestsuper",
        password=test_password,
        documento="87654321",
        email="email@testsuper.com",
        is_superuser = True
    )
    return user

@pytest.fixture
def test_password():
    return "secure_password_123"

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


# @pytest.fixture
# def get_user_generico():
#     test_user = create_user(username='test_user', documento_identidad='44635875', first_name='Test', last_name='User', email='test@user.com')
#     return test_user


@pytest.fixture
def get_authenticated_client(get_user_generico, api_client):
    refresh = RefreshToken.for_user(get_user_generico)
    access_token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return api_client

@pytest.fixture
def get_authenticated_client_and_user(get_user_generico, api_client):
    refresh = RefreshToken.for_user(get_user_generico)
    access_token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return get_user_generico, api_client

@pytest.fixture
def get_authenticated_admin_client(get_super_user, api_client):
    refresh = RefreshToken.for_user(get_super_user)
    access_token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return api_client


def get_auth_token(username, password, api_client):
    response = api_client.post('/api-token-auth/', data={
        'username': username,
        'password': password
    })
    assert response.status_code == 200
    return response.data['token']


def crear_token_usuario(usuario):
    token, _ = Token.objects.get_or_create(user=usuario)
    return token

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