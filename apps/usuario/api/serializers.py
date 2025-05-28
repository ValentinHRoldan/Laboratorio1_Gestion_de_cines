from rest_framework import serializers
from ..models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    password_confirmation = serializers.CharField(write_only=True)
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'apellido','documento','username', 'email', 'password', 'password_confirmation']

    def validate_documento(self, value):
        try:
            int(value)
        except ValueError:
            self.generarError("Documento invalido")
        return value
    
    def validate_email(self, value):
        if Usuario.objects.filter(email = value).exists():
            self.generarError("El email ya está en uso")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            self.generarError("La contraseña debe contener minimo 8 caracteres")
        return value
    
    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            self.generarError('Las contraseñas no coinciden')
        return data
    
    def create(self, validated_data):
        # Sacamos la password del validated_data
        password = validated_data.pop('password')
        validated_data.pop('password_confirmation')
        # Creamos el usuario SIN password
        user = Usuario(**validated_data)
        # Usamos set_password para encriptar
        user.set_password(password)
        user.save()
        return user
    
    def generarError(self, mensaje):
        raise serializers.ValidationError({
            'info': mensaje
        })