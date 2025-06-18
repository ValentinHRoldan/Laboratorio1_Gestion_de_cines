import pytest
from apps.funciones.models import Pelicula
from .fixtures_funcion import get_pelicula
from unittest.mock import MagicMock
from apps.funciones.servicios.tmdb import importar_peliculas_estreno
from decouple import config

@pytest.mark.django_db
def test_api_creacion_pelicula(get_pelicula):
    print(get_pelicula)
    assert Pelicula.objects.filter(titulo='Inception').exists()



@pytest.mark.django_db
def test_tmdb_api_llamada_correcta(mocker):
    api_key = config("TMDB_API_KEY")
    url_esperada = f"https://api.themoviedb.org/3/movie/now_playing?language=es-ES&region=AR&api_key={api_key}"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "results": [
            {
                "title": "Película TMDB",
                "overview": "Ultimo estreno",
                "poster_path": "/poster.jpg",
                "original_language": "es"
            }
        ]
    }

    mock_get = mocker.patch("apps.funciones.servicios.tmdb.requests.get"
, return_value=mock_response)

    importar_peliculas_estreno()

    mock_get.assert_called_once_with(url_esperada)