from django.db import models
    
class Asiento(models.Model):
    fila = models.CharField(max_length=5)
    numero = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.fila}{self.numero}"
    
class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()
    ubicacion = models.CharField(max_length=200)
    asientos = models.ManyToManyField(Asiento, related_name='salas_asiento')
    def __str__(self):
        return self.nombre


class Pelicula(models.Model):
    titulo = models.CharField(max_length=200, unique=True)
    duracion = models.PositiveIntegerField()
    genero = models.CharField(max_length=100)
    sinopsis = models.TextField()
    posters = models.URLField()
    clasificacion = models.CharField(max_length=50)
    idioma = models.CharField(max_length=50)
    trailer = models.URLField()

    def __str__(self):
        return self.titulo

    
class TipoFormato(models.Model):
    nombre = models.CharField(max_length=50, unique=True)  # Ej: "2D", "3D", "IMAX"
    precio = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

class Funcion(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='funciones')
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='funciones') 
    fecha = models.DateField()
    hora = models.TimeField()
    tipo_formato = models.ForeignKey(TipoFormato, on_delete=models.PROTECT, related_name='funciones')
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.pelicula.titulo} - {self.fecha} {self.hora}"