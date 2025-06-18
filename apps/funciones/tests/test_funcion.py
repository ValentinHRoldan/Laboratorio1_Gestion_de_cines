import pytest
from apps.funciones.models import Funcion
from .fixtures_funcion import get_funcion, get_pelicula, get_tipo_formato, get_peliculas
from .fixtures_sala import get_sala
from apps.usuario.tests.fixtures_user import get_authenticated_client, get_user_generico, test_password, grupo_usuarios_registrados, api_client, get_authenticated_admin_client, get_super_user
from rest_framework import status
from datetime import datetime, timezone

@pytest.mark.django_db
def test_creacion_funcion_orm(get_funcion):
    print(get_funcion)
    assert Funcion.objects.filter(sala=1).exists()

@pytest.mark.django_db
def test_api_creacion_funcion_admin(get_authenticated_admin_client, get_pelicula, get_sala, get_tipo_formato, mocker):
    client = get_authenticated_admin_client
    pelicula = get_pelicula
    sala = get_sala
    formato = get_tipo_formato

    fecha_actual_mock = datetime(2025, 6, 13, 21, 0, 0, tzinfo=timezone.utc)
    mocker.patch('django.utils.timezone.now', return_value=fecha_actual_mock)

    data = {
        "pelicula_id": pelicula.id,
        "sala_id": sala.id,
        "fecha": "2025-06-30",
        "hora": "20:00:00",
        "tipo_formato_id": formato.id,
        "activa": True
    }
    response = client.post(f'/api/funcion/', data=data)
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_api_creacion_funcion_usuario_registrado(get_authenticated_client, get_pelicula, get_sala, get_tipo_formato, mocker):
    client = get_authenticated_client
    pelicula = get_pelicula
    sala = get_sala
    formato = get_tipo_formato

    fecha_actual_mock = datetime(2025, 6, 13, 21, 0, 0, tzinfo=timezone.utc)
    mocker.patch('django.utils.timezone.now', return_value=fecha_actual_mock)

    data = {
        "pelicula_id": pelicula.id,
        "sala_id": sala.id,
        "fecha": "2025-06-30",
        "hora": "20:00:00",
        "tipo_formato_id": formato.id,
        "activa": True
    }
    response = client.post(f'/api/funcion/', data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_api_modificacion_funcion(get_authenticated_admin_client, get_peliculas, get_sala, get_tipo_formato, mocker, get_funcion):
    client = get_authenticated_admin_client
    pelicula1, pelicula2, pelicula3 = get_peliculas
    sala = get_sala
    formato = get_tipo_formato

    fecha_actual_mock = datetime(2025, 6, 13, 21, 0, 0, tzinfo=timezone.utc)
    mocker.patch('django.utils.timezone.now', return_value=fecha_actual_mock)

    data = {
        "pelicula": pelicula2.id,
        "fecha": "2025-06-27"
    }
    response = client.patch(f'/api/funcion/{get_funcion.id}/', data=data)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_api_eliminacion_funcion_admin(get_authenticated_admin_client, get_peliculas, get_sala, get_tipo_formato, mocker, get_funcion):
    client = get_authenticated_admin_client

    response = client.delete(f'/api/funcion/{get_funcion.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
def test_api_eliminacion_funcion_usuario_registrado(get_authenticated_client, get_peliculas, get_sala, get_tipo_formato, mocker, get_funcion):
    client = get_authenticated_client

    response = client.delete(f'/api/funcion/{get_funcion.id}/')
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_api_listar_funciones(get_authenticated_client):
    client = get_authenticated_client

    response = client.get(f'/api/funcion/')
    assert response.status_code == status.HTTP_200_OK