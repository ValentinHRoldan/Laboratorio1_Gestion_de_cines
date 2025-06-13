import pytest
from django.urls import reverse
from apps.usuario.models import Usuario

@pytest.mark.django_db
def test_login_usuario(client, create_user, test_password):
    user = create_user
    url = reverse('usuario:login')

    response = client.post(url, {
        'username': user.username,
        'password': test_password
    })
    assert response.status_code == 200

@pytest.mark.django_db
def test_registro_usuario(client, grupo_usuarios_registrados, test_password):
    url = reverse('usuario:register')
    datos_usuario = {
        'nombre': 'NuevoNombre',
        'apellido': 'NuevoApellido',
        'username': 'nuevo_usuario',  # distinto
        'password': test_password,
        'password_confirmation': test_password,
        'documento': '98765432',
        'email': 'nuevo@email.com',  # distinto
    }
    response = client.post(url, datos_usuario)
    assert response.status_code == 201
    # se verifica si el usuario creado existe 
    assert Usuario.objects.filter(username='nuevo_usuario').exists()

    # Verifica contenido de la respuesta
    # Por ejemplo, que contenga el ID del nuevo usuario o un token de autenticación
    # data = response.json()
    # assert 'id' in data or 'token' in data