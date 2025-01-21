from typing import Any
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone

# Create your models here.
class UserAccountManager(BaseUserManager):
    def create_user(self, id_documento, password=None, **kwargs):
        

        user = self.model(
            id_documento=id_documento,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id_documento, password=None, **kwargs):
        user = self.create_user(id_documento=id_documento, password=password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Usuario(AbstractBaseUser, PermissionsMixin):

    nombres = models.CharField(max_length=255, db_column='nombre')
    apellidos = models.CharField(max_length=255, db_column='apellido')
    id_documento = models.CharField(max_length=255, unique=True, db_column='id_documento')
    tipo_documento = models.CharField(max_length=50, db_column='tipo_documento')
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now, db_column='fecha_registro')
    last_login = models.DateTimeField(default=timezone.now, db_column='ultimo_inicio_sesion', blank=True, null=True)
    rol = models.ForeignKey('Rol', models.CASCADE, db_column='id_rol', blank=True, null=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'id_documento'
    REQUIRED_FIELDS = ['nombres', 'apellidos' ,'email','tipo_documento']

    class Meta:
        db_table = 'Usuario'
        managed = True

    def save(self, *args, **kwargs):
        if not self.rol:
            default_rol, created = Rol.objects.get_or_create(
                nombre='paciente',
                defaults={'descripcion': 'Rol por defecto para nuevos usuarios'}
            )
            self.rol = default_rol
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True, db_column='id_rol')
    nombre = models.CharField(max_length=255, db_column='nombre')
    descripcion = models.CharField(max_length=255, blank=True, null=True, db_column='descripcion')

    class Meta:
        managed = True
        db_table = 'Rol'

    def __str__(self):
        return self.nombre


class UsuarioContacto(models.Model):
    usuario = models.OneToOneField(Usuario, models.CASCADE, db_column='id_usuario', blank=True, null=True, related_name='usuariocontacto')
    telefono = models.CharField(max_length=50, blank=True, null=True, db_column='telefono')
    direccion = models.CharField(max_length=255, blank=True, null=True, db_column='direccion')
    ciudad = models.CharField(max_length=50, blank=True, null=True, db_column='ciudad')


    class Meta:
        managed = True
        db_table = 'Usuario_contacto'

    def __str__(self):
        return f"Contacto de {self.id_usuario}"


class UsuarioInformacionPersonal(models.Model):
    usuario = models.OneToOneField(Usuario, models.CASCADE, db_column='id_usuario', related_name='usuarioinformacionpersonal')
    fecha_nacimiento = models.DateTimeField(blank=True, null=True, db_column='fecha_nacimiento')
    estado_civil = models.CharField(max_length=50, blank=True, null=True, db_column='estado_civil')
    genero = models.CharField(max_length=50, blank=True, null=True, db_column='genero')
    ocupacion = models.CharField(max_length=100, blank=True, null=True, db_column='ocupacion')
    tipo_sangre = models.CharField(max_length=10, blank=True, null=True, db_column='tipo_sangre')
    triage = models.CharField(max_length=50, blank=True, null=True, db_column='triage')

    class Meta:
        managed = True
        db_table = 'Usuario_informacion_personal'

    def __str__(self):
        return f"Información Personal de {self.id_documento}"
