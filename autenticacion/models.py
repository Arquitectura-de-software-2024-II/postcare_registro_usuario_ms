from django.db import models


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Rol'


class Usuario(models.Model):
    id_documento = models.AutoField(primary_key=True)
    id_rol = models.ForeignKey(Rol, models.DO_NOTHING, db_column='id_rol', blank=True, null=True)
    contrasena = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    fecha_registro = models.DateField(blank=True, null=True)
    ultimo_inicio_sesion = models.DateField(blank=True, null=True)
    estado_cuenta = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Usuario'


class UsuarioContacto(models.Model):
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Usuario_contacto'


class UsuarioInformacionPersonal(models.Model):
    id_documento = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_documento')
    tipo_documento = models.CharField(max_length=50)
    fecha_nacimiento = models.DateTimeField(blank=True, null=True)
    estado_civil = models.CharField(max_length=50, blank=True, null=True)
    genero = models.CharField(max_length=50, blank=True, null=True)
    ocupacion = models.CharField(max_length=100, blank=True, null=True)
    tipo_sangre = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Usuario_informacion_personal'
