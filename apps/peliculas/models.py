from django.db import models

class Pelicula(models.Model):
    titulo = models.CharField(max_length=200)
    duracion = models.PositiveIntegerField()
    genero = models.CharField(max_length=100)
    sinopsis = models.TextField()
    posters = models.URLField()
    clasificacion = models.CharField(max_length=50)
    idioma = models.CharField(max_length=50)
    trailer = models.URLField()

    def __str__(self):
        return self.titulo

