import pytest
from .fixtures_user import get_authenticated_client, get_user_generico, api_client, api_client
from ..models import Anuncio, OfertaAnuncio
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