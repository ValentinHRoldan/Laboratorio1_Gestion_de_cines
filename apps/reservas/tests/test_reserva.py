import pytest

from apps.funciones.models import Asiento, Funcion, Pelicula, Sala, TipoFormato
from apps.reservas.models import Reserva
from .fixtures_user import get_authenticated_client, get_user_generico, api_client, api_client
from .fixtures_funcion import get_tipo_formato, get_pelicula, get_funcion
from .fixtures_sala import get_sala, get_asiento, get_asientos
from .fixtures_reserva import get_reserva
from apps.usuario.models import Usuario

def test_foo():
    assert True


def test_lista():
    assert list(reversed([1, 2, 3])) == [3, 2, 1]

@pytest.mark.django_db
def test_api_creacion_anuncio(get_authenticated_client): #1.1
    client = get_authenticated_client

    data = {
        "nombre": "Equipo deportivo",
    }

    response = client.post(f'/api/categoria/', data=data)

    data = {
        "titulo": "par de mancuernas",
        "descripcion": "de 5kg c/u",
        "precio_inicial": "30000",
        "fecha_inicio": "2025-06-15",
        "fecha_fin": "2025-06-30",
        "categorias_ids": [
            1
        ]
    }
    print(client._credentials)
    response = client.post(f'/api/anuncio/', data=data)
    assert response.status_code == 201
    assert Anuncio.objects.filter(titulo='par de mancuernas').count() == 1

@pytest.mark.django_db
def test_api_mod_anuncio(get_authenticated_client,get_categoria): #2.1

    client = get_authenticated_client

    data = {
        "titulo": "par de mancuernas",
        "descripcion": "de 5kg c/u",
        "precio_inicial": "30000",
        "fecha_inicio": "2025-06-15",
        "fecha_fin": "2025-06-30",
        "categorias_ids": [
            1
        ]
    }

    response = client.post(f'/api/anuncio/', data=data)

    data = {
        "descripcion": "de 5.5kg c/u",
        "precio_inicial": "32000",
    }
    print(client._credentials)
    response = client.patch(f'/api/anuncio/1/', data=data)
    assert response.status_code == 200
    assert Anuncio.objects.filter(titulo='par de mancuernas').count() == 1

@pytest.mark.django_db
def test_api_lista_anuncios(get_authenticated_client, get_anuncio): #3.1
    cliente = get_authenticated_client

    anuncio = get_anuncio

    response = cliente.get(f'/api/anuncio/')
    assert response.status_code == 200

    data = response.data
    assert data[0]['titulo'] == anuncio.titulo

@pytest.mark.django_db
def test_api_creacion_oferta_anuncio(get_authenticated_client, get_categoria, get_anuncio): #4.1
    client = get_authenticated_client

    data = {
        "precio_oferta": "150001"
    }

    response = client.post(f'/api/anuncio/1/ofertar/', data=data)
    assert response.status_code == 201
    assert OfertaAnuncio.objects.filter(precio_oferta='150001',anuncio=get_anuncio).count() == 1


@pytest.mark.django_db
def test_api_fallo_creacion_oferta_anuncio_datos_invalidos(get_authenticated_client, get_categoria, get_anuncio): #4.2
    client = get_authenticated_client

    data = {
        "precio_oferta": "149999.99"
    }

    response = client.post(f'/api/anuncio/1/ofertar/', data=data)
    
    # assert response.status_code == 400

    # assert OfertaAnuncio.objects.filter(precio_oferta='149999.99').count() == 0

    # assert 'La oferta debe ser mayor al precio inicial del artículo.' in str(response.content)

@pytest.mark.django_db
def test_api_creacion_usuario(get_authenticated_client, get_user_generico):
    assert Usuario.objects.filter(username='test_user').exists()


@pytest.mark.django_db
def test_api_creacion_formato(get_tipo_formato):
    print(get_tipo_formato)
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
def test_api_creacion_asiento(get_asiento):
    print(get_asiento)
    assert Asiento.objects.filter(fila='C').exists()

@pytest.mark.django_db
def test_api_creacion_funcion(get_funcion):
    print(get_funcion)
    assert Funcion.objects.filter(sala=1).exists()

@pytest.mark.django_db
def test_api_creacion_reserva(get_reserva):
    print(get_reserva)
    assert Reserva.objects.filter(funcion=1).exists() 