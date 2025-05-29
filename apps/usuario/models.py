from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class Usuario(AbstractUser):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    documento = models.CharField(max_length=8, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.username}'