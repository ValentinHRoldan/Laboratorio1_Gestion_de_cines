from datetime import datetime, timezone
import pytest

from apps.funciones.models import Asiento, Funcion, Pelicula, Sala, TipoFormato
from apps.reservas.models import AsientoReservado, Reserva
from .fixtures_user import get_authenticated_client, get_authenticated_admin_client, get_user_generico, api_client, get_super_user, test_password, grupo_usuarios_registrados, get_authenticated_client_and_user
from .fixtures_funcion import get_tipo_formato, get_tipos_formatos, get_pelicula, get_peliculas, get_funcion, get_funciones, get_funcion_pasada, get_funcion_
from .fixtures_sala import get_sala, get_salas, get_asiento, get_asientos, get_asiento_
from .fixtures_reserva import get_reserva, get_reservas
from apps.usuario.models import Usuario
from rest_framework import status

def test_foo():
    assert True


def test_lista():
    assert list(reversed([1, 2, 3])) == [3, 2, 1]

#LISTAR RESERVA CON USUARIO ADMIN

@pytest.mark.django_db
def test_api_listar_reservas(get_authenticated_admin_client, get_reservas):
    
    client = get_authenticated_admin_client

    response = client.get(f'/api/reserva/')

    assert response.status_code == 200

    data = response.data

    print(Reserva.objects.all())

    assert len(data['results']) == len(get_reservas)

    # Extraemos los IDs del response
    response_ids = {reserva['id'] for reserva in data['results']}
    reservas_ids = {reserva.id for reserva in get_reservas}
    # Comparamos que los conjuntos de IDs sean iguales
    assert response_ids == reservas_ids

#LISTAR RESERVA CON USUARIO GENERICO

@pytest.mark.django_db
def test_api_listar_reservas2(get_authenticated_client, get_reservas):
    
    client = get_authenticated_client

    response = client.get(f'/api/reserva/')

    assert response.status_code == 200

    data = response.data

    print(Reserva.objects.all())

    assert len(data['results']) != len(get_reservas)

    # Extraemos los IDs del response
    response_ids = {reserva['id'] for reserva in data['results']}
    reservas_ids = {reserva.id for reserva in get_reservas}
    
    assert response_ids != reservas_ids

#LISTAR RESERVA CON USUARIO NO AUTENTICADO

@pytest.mark.django_db
def test_api_listar_reservas_falla_usuario_no_autenticado(api_client, get_reservas):
    response = api_client.get(f'/api/reserva/')

    assert response.status_code == 401
    assert str(response.data['detail']) == "Authentication credentials were not provided."

#CREACION DE RESERVA

@pytest.mark.django_db
def test_api_creacion_reserva(mocker, get_authenticated_client, get_asientos, get_funcion):
    
    client = get_authenticated_client

    asiento1, asiento2, asiento3 = get_asientos

    funcion = get_funcion

    fecha_actual_mock = datetime(2025, 6, 13, 21, 0, 0, tzinfo=timezone.utc)
    mocker.patch('django.utils.timezone.now', return_value=fecha_actual_mock)

    data = {
        "funcion_id": funcion.id,
        "cantidad_entradas": 3,
        "asientos": [asiento1.id, asiento2.id, asiento3.id]
    }

    response = client.post(f'/api/reserva/', data=data)

    assert response.status_code == 201

    assert Reserva.objects.filter(
        funcion=funcion,
        funcion__activa=True,
        asientos_reservados__asiento__in=[asiento1, asiento2, asiento3]
    ).count() == 1

#CREACION DE RESERVA DE FUNCION PASADA

@pytest.mark.django_db
def test_api_creacion_reserva_falla_funcion_pasada(mocker, get_authenticated_client, get_asientos, get_funcion_pasada):
    
    client = get_authenticated_client

    asiento1, asiento2, asiento3 = get_asientos

    funcion = get_funcion_pasada

    fecha_actual_mock = datetime(2025, 6, 13, 21, 0, 0, tzinfo=timezone.utc)
    mocker.patch('django.utils.timezone.now', return_value=fecha_actual_mock)

    data = {
        "funcion_id": funcion.id,
        "cantidad_entradas": 3,
        "asientos": [asiento1.id, asiento2.id, asiento3.id]
    }

    response = client.post(f'/api/reserva/', data=data)

    assert response.status_code == 400
    assert str(response.data['funcion_id']['info']) == "La función ya pasó."

#RESERVA ASIENTO YA RESERVADO DE UNA FUNCION

@pytest.mark.django_db
def test_api_creacion_reserva_falla_asiento_ocupado(mocker, get_authenticated_client, get_asientos, get_reserva, get_funcion):
    
    client = get_authenticated_client

    asiento, _,_= get_asientos

    funcion = get_funcion

    fecha_actual_mock = datetime(2025, 6, 13, 21, 0, 0, tzinfo=timezone.utc)
    mocker.patch('django.utils.timezone.now', return_value=fecha_actual_mock)

    data = {
        "funcion_id": funcion.id,
        "cantidad_entradas": 1,
        "asientos": [asiento.id]
    }

    response = client.post(f'/api/reserva/', data=data)

    assert response.status_code == 400

    assert str(response.data[0]) == "El asiento C1 ya está reservado para esta función."

#RESERVA DE MAS ASIENTOS QUE LOS SOLICITADOS

@pytest.mark.django_db
def test_api_creacion_reserva_falla_asientos_de_mas(mocker, get_authenticated_client, get_asientos, get_reserva, get_funcion):
    
    client = get_authenticated_client

    asiento1, asiento2,_= get_asientos

    funcion = get_funcion

    fecha_actual_mock = datetime(2025, 6, 13, 21, 0, 0, tzinfo=timezone.utc)
    mocker.patch('django.utils.timezone.now', return_value=fecha_actual_mock)

    data = {
        "funcion_id": funcion.id,
        "cantidad_entradas": 1,
        "asientos": [asiento1.id, asiento2.id]
    }

    response = client.post(f'/api/reserva/', data=data)

    assert response.status_code == 400

    assert str(response.data['info'][0]) == "La cantidad de asientos no coincide con la cantidad de entradas."

#MODIFICACIÓN DE RESERVA

@pytest.mark.django_db
def test_api_modificacion_reserva(mocker, get_authenticated_client, get_reserva, get_asientos):
    
    client = get_authenticated_client

    asiento1, asiento2, asiento3 = get_asientos

    fecha_actual_mock = datetime(2025, 6, 13, 21, 0, 0, tzinfo=timezone.utc)
    mocker.patch('django.utils.timezone.now', return_value=fecha_actual_mock)

    data = {
        "cantidad_entradas": 2,
        "asientos": [asiento1.id, asiento2.id]
    }

    response = client.patch(f'/api/reserva/{get_reserva.id}/', data=data)

    assert response.status_code == 200
    assert response.data['id'] == get_reserva.id
    assert response.data['cantidad_entradas'] == 2
    ids_en_response = [a['asiento']['id'] for a in response.data['asientos_reservados']]
    assert ids_en_response == [asiento1.id, asiento2.id]

#MODIFICACIÓN DE RESERVA DE OTRO USUARIO

@pytest.mark.django_db
def test_api_modificacion_reserva_agena(mocker, get_authenticated_client_and_user, get_reservas, get_asientos):
    
    user, client = get_authenticated_client_and_user
    reserva1, reserva2, reserva3 = get_reservas
    asiento1, asiento2, asiento3 = get_asientos

    fecha_actual_mock = datetime(2025, 6, 13, 21, 0, 0, tzinfo=timezone.utc)
    mocker.patch('django.utils.timezone.now', return_value=fecha_actual_mock)

    data = {
        "cantidad_entradas": 2,
        "asientos": [asiento1.id, asiento2.id]
    }

    response = client.patch(f'/api/reserva/{reserva2.id}/', data=data)
    
    assert response.status_code == 404
    assert reserva2.usuario != user

#ELIMINACIÓN DE RESERVA

@pytest.mark.django_db
def test_api_eliminacion_reserva(get_authenticated_client, get_reserva):
    
    client = get_authenticated_client

    response = client.delete(f'/api/reserva/{get_reserva.id}/')

    assert response.status_code == 204
    assert Reserva.objects.filter(id=get_reserva.id).count() == 0

#-----------------

@pytest.mark.django_db
def test_api_creacion_usuario(get_authenticated_client):
    assert Usuario.objects.filter(username='testuser').exists()

@pytest.mark.django_db
def test_api_creacion_usuario2(get_user_generico):
    print(get_user_generico)
    print(get_user_generico.user_permissions.all())
    assert Usuario.objects.filter(username='testuser').exists()

@pytest.mark.django_db
def test_api_creacion_formato(get_tipo_formato):
    print(get_tipo_formato)
    assert TipoFormato.objects.filter(nombre='2D').exists()

@pytest.mark.django_db
def test_api_creacion_formatos(get_tipos_formatos):
    print(get_tipos_formatos)
    assert TipoFormato.objects.filter(nombre='2D').exists()

@pytest.mark.django_db
def test_api_creacion_pelicula(get_pelicula):
    print(get_pelicula)
    assert Pelicula.objects.filter(titulo='Inception').exists()

@pytest.mark.django_db
def test_api_creacion_sala(get_sala):
    print(get_sala)
    assert Sala.objects.filter(ubicacion='Piso 1 - A').exists()

@pytest.mark.django_db
def test_api_creacion_salas(get_salas):
    print(get_salas)
    assert Sala.objects.filter(ubicacion='Piso 1 - A').exists()

@pytest.mark.django_db
def test_api_creacion_asiento(get_asiento):
    print(get_asiento)
    assert Asiento.objects.filter(fila='C').exists()

@pytest.mark.django_db
def test_api_creacion_asientos(get_asientos):
    print(get_asientos)
    assert Asiento.objects.filter(fila='C').exists()

@pytest.mark.django_db
def test_api_creacion_funcion(get_funcion):
    print(get_funcion)
    assert Funcion.objects.filter(sala=1).exists()

@pytest.mark.django_db
def test_api_creacion_reservaf(get_reserva):
    print(get_reserva)
    assert Reserva.objects.filter(funcion=1).exists()

@pytest.mark.django_db
def test_reserva_asiento_no_perteneciente_sala(get_authenticated_client, get_asiento_, get_salas, get_asiento, get_funcion, mocker):
    cliente = get_authenticated_client
    funcion = get_funcion
    sala1, sala2, sala3 = get_salas
    asientoAjeno = get_asiento_(sala=sala2)
    asientoValido = get_asiento

    fecha_actual_mock = datetime(2025, 6, 13, 21, 0, 0, tzinfo=timezone.utc)
    mocker.patch('django.utils.timezone.now', return_value=fecha_actual_mock)

    data = {
        "funcion_id": funcion.id,
        "cantidad_entradas": 1,
        "asientos": [asientoAjeno.id]        
    }
    response = cliente.post(f'/api/reserva/', data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert str(response.data[0]) == 'El asiento C2 no pertenece a la sala de la función.'
    assert asientoAjeno.sala != (asientoValido.sala == funcion.sala)

@pytest.mark.django_db
def test_reserva_misma_sala_diferente_funcion(get_authenticated_client, get_salas, get_peliculas, get_funcion_, mocker, get_asiento):
    client = get_authenticated_client
    sala1, sala2, sala3 = get_salas
    pelicula1, pelicula2, pelicula3 = get_peliculas
    funcion = get_funcion_(pelicula=pelicula1, sala=sala1, fecha="2025-06-15")
    funcion2 = get_funcion_(pelicula=pelicula2, sala=sala1, fecha="2025-06-16")
    asiento = get_asiento

    fecha_actual_mock = datetime(2025, 6, 13, 21, 0, 0, tzinfo=timezone.utc)
    mocker.patch('django.utils.timezone.now', return_value=fecha_actual_mock)

    data = {
        "funcion_id": funcion.id,
        "cantidad_entradas": 1,
        "asientos": [asiento.id]        
    }
    response = client.post(f'/api/reserva/', data=data)
    assert response.status_code == status.HTTP_201_CREATED

    data = {
        "funcion_id": funcion2.id,
        "cantidad_entradas": 1,
        "asientos": [asiento.id]        
    }
    response = client.post(f'/api/reserva/', data=data)
    assert response.status_code == status.HTTP_201_CREATED

