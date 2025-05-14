import requests
from ..models import Pelicula
from decouple import config
 
API_KEY = config("TMDB_API_KEY") 
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
                    "duracion": 120,  # valor prefedinido, despues solucionamos
                    "genero": "Acción",  
                    "sinopsis": peli.get("overview", ""),
                    "posters": IMG_URL + peli["poster_path"] if peli.get("poster_path") else "",
                    "clasificacion": "General",  # valor prefedinido, despues solucionamos
                    "idioma": peli.get("original_language", "es"),
                    "trailer": ""  
                }
            )
    else:
        print(f"Error al obtener películas: {response.status_code}")
