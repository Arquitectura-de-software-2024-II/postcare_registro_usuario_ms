from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, email, contrasena=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(contrasena)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, contrasena=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, contrasena, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    id_documento = models.AutoField(primary_key=True, db_column='id_documento')
    email = models.EmailField(unique=True, db_column='email')
    password = models.CharField(max_length=255, db_column='contrasena')
    nombre = models.CharField(max_length=255, db_column='nombre')
    apellido = models.CharField(max_length=255, db_column='apellido')
    is_active = models.BooleanField(default=True, db_column='estado_cuenta')
    is_staff = models.BooleanField(default=False, db_column='is_staff')
    is_superuser = models.BooleanField(default=False, db_column='is_superuser')
    date_joined = models.DateTimeField(default=timezone.now, db_column='fecha_registro')
    last_login = models.DateTimeField(default=timezone.now, db_column='ultimo_inicio_sesion', blank=True, null=True)
    
    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    class Meta:
        db_table = 'Usuario'
        managed = False

    def __str__(self):
        return self.email


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True, db_column='id_rol')
    nombre = models.CharField(max_length=255, db_column='nombre')
    descripcion = models.CharField(max_length=255, blank=True, null=True, db_column='descripcion')

    class Meta:
        managed = False
        db_table = 'Rol'

    def __str__(self):
        return self.nombre

class UsuarioContacto(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Usuario_contacto'

    def __str__(self):
        return f"Contacto de {self.id_usuario}"

class UsuarioInformacionPersonal(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    id_documento = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_documento')
    tipo_documento = models.CharField(max_length=50, db_column='tipo_documento')
    fecha_nacimiento = models.DateTimeField(blank=True, null=True, db_column='fecha_nacimiento')
    estado_civil = models.CharField(max_length=50, blank=True, null=True, db_column='estado_civil')
    genero = models.CharField(max_length=50, blank=True, null=True, db_column='genero')
    ocupacion = models.CharField(max_length=100, blank=True, null=True, db_column='ocupacion')
    tipo_sangre = models.CharField(max_length=10, blank=True, null=True, db_column='tipo_sangre')

    class Meta:
        managed = False
        db_table = 'Usuario_informacion_personal'

    def __str__(self):
        return f"Información Personal de {self.id_documento}"
