# autenticacion/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Rol

@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    if sender.name == 'autenticacion':
        Rol.objects.get_or_create(nombre='administrador', defaults={'descripcion': 'Rol de administrador'})
        Rol.objects.get_or_create(nombre='paciente', defaults={'descripcion': 'Rol por defecto para nuevos usuarios'})
