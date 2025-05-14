from rest_framework import serializers
from ..models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        # Sacamos la password del validated_data
        password = validated_data.pop('password')
        # Creamos el usuario SIN password
        user = Usuario(**validated_data)
        # Usamos set_password para encriptar
        user.set_password(password)
        user.save()
        return user