from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# class UsuarioManager(BaseUserManager):
#     use_in_migrations = True

#     def create_user(self, username, email=None, password=None, **extra_fields):
#         if not username:
#             raise ValueError('El nombre de usuario debe ser obligatorio')
#         if not extra_fields.get('documento_identidad'):
#             raise ValueError('El documento de identidad es obligatorio')
#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('El superusuario debe tener is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('El superusuario debe tener is_superuser=True.')

#         return self.create_user(username, email, password, **extra_fields)


class Usuario(AbstractUser):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    documento = models.CharField(max_length=8, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.username}'