from rest_framework import serializers
from .models import Usuario, UsuarioInformacionPersonal, UsuarioContacto , Rol

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'email', 'tipo_documento']

class UsuarioInformacionPersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioInformacionPersonal
        fields = ['fecha_nacimiento', 'estado_civil', 'genero', 'ocupacion', 'tipo_sangre']

class UsuarioContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioContacto
        fields = ['telefono', 'direccion', 'ciudad']

class UsuarioRolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion']

class UsuarioInformacionMeSerializer(serializers.ModelSerializer):
    informacion_personal = UsuarioInformacionPersonalSerializer(source='usuarioinformacionpersonal', read_only=True)
    contacto = UsuarioContactoSerializer(source='usuariocontacto', read_only=True)
    user_rol = UsuarioRolSerializer(source='rol', read_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'nombres', 'apellidos', 'email', 'tipo_documento','user_rol', 'informacion_personal', 'contacto']

