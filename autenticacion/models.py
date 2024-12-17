from typing import Any
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone

# Create your models here.
class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(email, password=password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, default=1)
    first_name = models.CharField(max_length=255, default='default_first_name')
    last_name = models.CharField(max_length=255, default='default_first_name')
    email = models.EmailField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now, db_column='fecha_registro')
    last_login = models.DateTimeField(default=timezone.now, db_column='ultimo_inicio_sesion', blank=True, null=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'Usuario'
        managed = True

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
    id_usuario = models.ForeignKey(Usuario, models.CASCADE, db_column='id_usuario', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Usuario_contacto'

    def __str__(self):
        return f"Contacto de {self.id_usuario}"


class UsuarioInformacionPersonal(models.Model):
    id_documento = models.ForeignKey(Usuario, models.CASCADE, db_column='id_documento')
    tipo_documento = models.CharField(max_length=50, db_column='tipo_documento')
    fecha_nacimiento = models.DateTimeField(blank=True, null=True, db_column='fecha_nacimiento')
    estado_civil = models.CharField(max_length=50, blank=True, null=True, db_column='estado_civil')
    genero = models.CharField(max_length=50, blank=True, null=True, db_column='genero')
    ocupacion = models.CharField(max_length=100, blank=True, null=True, db_column='ocupacion')
    tipo_sangre = models.CharField(max_length=10, blank=True, null=True, db_column='tipo_sangre')

    class Meta:
        managed = True
        db_table = 'Usuario_informacion_personal'

    def __str__(self):
        return f"Información Personal de {self.id_documento}"
