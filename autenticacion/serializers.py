from rest_framework import serializers
from .models import Usuario, UsuarioInformacionPersonal, UsuarioContacto , Rol

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'email', 'tipo_documento']

class UsuarioInformacionPersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioInformacionPersonal
        fields = ['fecha_nacimiento', 'estado_civil', 'genero', 'ocupacion', 'tipo_sangre','triage']

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
        fields = ['id', 'id_documento','nombres', 'apellidos', 'email', 'tipo_documento','user_rol', 'informacion_personal', 'contacto']


class PacienteSerializer(serializers.ModelSerializer):
    triage = serializers.CharField(source='usuarioinformacionpersonal.triage')

    class Meta:
        model = Usuario
        fields = ['id', 'id_documento', 'nombres', 'apellidos', 'email', 'triage']

class UsuarioDetalleSerializer(serializers.ModelSerializer):
    informacion_personal = UsuarioInformacionPersonalSerializer(source='usuarioinformacionpersonal', read_only=True)
    contacto = UsuarioContactoSerializer(source='usuariocontacto', read_only=True)
    user_rol = UsuarioRolSerializer(source='rol', read_only=True)

    class Meta:
        model = Usuario
        fields = ['id','id_documento', 'nombres', 'apellidos', 'email', 'tipo_documento', 'user_rol', 'informacion_personal', 'contacto']

class ChangeUserRoleSerializer(serializers.Serializer):
    rol = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_rol(self, value):
        if value not in ['administrador', 'paciente']:
            raise serializers.ValidationError("Rol inválido.")
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        password = attrs.get('password')

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Contraseña incorrecta."})

        return attrs
    
class ChangeUserTriageSerializer(serializers.Serializer):
    triage = serializers.CharField(max_length=50)

    def validate_id_usuario(self, value):
        if not UsuarioInformacionPersonal.objects.filter(usuario__id=value).exists():
            raise serializers.ValidationError("Usuario no encontrado.")
        return value
    

class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioContacto
        fields = ['telefono']