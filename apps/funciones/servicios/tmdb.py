# services/tmdb.py (o donde prefieras organizarlo)
import requests
from ..models import Pelicula  # ajusta si tu app no se llama "peliculas"
from decouple import config
 
API_KEY = config("TMDB_API_KEY")  # reemplaza con tu clave
BASE_URL = "https://api.themoviedb.org/3"
IMG_URL = "https://image.tmdb.org/t/p/w500"

def importar_peliculas_estreno():
    url = f"{BASE_URL}/movie/now_playing?language=es-ES&region=AR&api_key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        peliculas = data.get("results", [])

        for peli in peliculas:
            Pelicula.objects.get_or_create(
                titulo=peli["title"],
                defaults={
                    "duracion": 120,  # valor por defecto
                    "genero": "Acción",  # opcional: puedes dejarlo así o mejorar luego
                    "sinopsis": peli.get("overview", ""),
                    "posters": IMG_URL + peli["poster_path"] if peli.get("poster_path") else "",
                    "clasificacion": "General",  # valor por defecto
                    "idioma": peli.get("original_language", "es"),
                    "trailer": ""  # lo dejamos vacío
                }
            )
    else:
        print(f"Error al obtener películas: {response.status_code}")
