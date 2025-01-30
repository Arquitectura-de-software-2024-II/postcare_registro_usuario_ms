from rest_framework.permissions import BasePermission
from .models import Rol

class IsAdministrador(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.rol.nombre == 'administrador'