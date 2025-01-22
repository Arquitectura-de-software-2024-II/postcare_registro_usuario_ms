#from django.shortcuts import render
# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from djoser.social.views import ProviderAuthView
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from .serializers import(
    UsuarioSerializer,
    UsuarioInformacionPersonalSerializer,
    UsuarioContactoSerializer,
    UsuarioInformacionMeSerializer,
    PacienteSerializer,
    UsuarioDetalleSerializer
)
from .models import UsuarioInformacionPersonal, UsuarioContacto, Usuario
from djoser.views import UserViewSet
from .permissions import IsAdministrador

class CustomProviderAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)


        if response.status_code == 201:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')


            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )


            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )


        return response

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            response.set_cookie(
                'access', 
                access_token, 
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE, 
                path=settings.AUTH_COOKIE_PATH, 
                secure=settings.AUTH_COOKIE_SECURE, 
                httponly=settings.AUTH_COOKIE_HTTP_ONLY, 
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh', 
                refresh_token, 
                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE, 
                path=settings.AUTH_COOKIE_PATH, 
                secure=settings.AUTH_COOKIE_SECURE, 
                httponly=settings.AUTH_COOKIE_HTTP_ONLY, 
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
        return response

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')
        if refresh_token:
            request.data['refresh'] = refresh_token
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get('access')
            response.set_cookie(
                'access', 
                access_token, 
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE, 
                path=settings.AUTH_COOKIE_PATH, 
                secure=settings.AUTH_COOKIE_SECURE, 
                httponly=settings.AUTH_COOKIE_HTTP_ONLY, 
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
        return response

class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')
        if access_token:
            request.data['token'] = access_token
        return super().post(request, *args, **kwargs)

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response
    
class CustomUserViewSet(UserViewSet):
    def me(self, request, *args, **kwargs):
        user = request.user
        serializer = UsuarioInformacionMeSerializer(user)
        return Response(serializer.data)


class UserFormInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        personal_info_data = request.data.get('informacion_personal')
        contacto_data = request.data.get('contacto')

        personal_info_data['usuario'] = user.id
        contacto_data['usuario'] = user.id

        personal_info_instance, _ = UsuarioInformacionPersonal.objects.get_or_create(usuario=user)
        contacto_instance, _ = UsuarioContacto.objects.get_or_create(usuario=user)

        personal_info_serializer = UsuarioInformacionPersonalSerializer(personal_info_instance, data=personal_info_data)
        contacto_serializer = UsuarioContactoSerializer(contacto_instance, data=contacto_data)

        if personal_info_serializer.is_valid() and contacto_serializer.is_valid():
            personal_info_serializer.save()
            contacto_serializer.save()
            return Response({
                'informacion_personal': personal_info_serializer.data,
                'contacto': contacto_serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'informacion_personal': personal_info_serializer.errors,
            'contacto': contacto_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

class UpdateUserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user_data = request.data.get('usuario', {})
        personal_info_data = request.data.get('informacion_personal', {})
        contacto_data = request.data.get('contacto', {})

        if personal_info_data:
            personal_info_data['id_documento'] = user.id
        if contacto_data:
            contacto_data['id_usuario'] = user.id

        user_serializer = UsuarioSerializer(user, data=user_data, partial=True)
        personal_info_instance, _ = UsuarioInformacionPersonal.objects.get_or_create(usuario=user)
        contacto_instance, _ = UsuarioContacto.objects.get_or_create(usuario=user)

        personal_info_serializer = UsuarioInformacionPersonalSerializer(personal_info_instance, data=personal_info_data, partial=True)
        contacto_serializer = UsuarioContactoSerializer(contacto_instance, data=contacto_data, partial=True)

        if user_serializer.is_valid() and personal_info_serializer.is_valid() and contacto_serializer.is_valid():
            user_serializer.save()
            personal_info_serializer.save()
            contacto_serializer.save()
            return Response({
                'usuario': user_serializer.data,
                'informacion_personal': personal_info_serializer.data,
                'contacto': contacto_serializer.data
            }, status=status.HTTP_200_OK)
        
        errors = {}
        if not user_serializer.is_valid():
            errors['usuario'] = user_serializer.errors
        if not personal_info_serializer.is_valid():
            errors['informacion_personal'] = personal_info_serializer.errors
        if not contacto_serializer.is_valid():
            errors['contacto'] = contacto_serializer.errors
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class ListaPacientesView(generics.ListAPIView):
    serializer_class = PacienteSerializer
    permission_classes = [IsAdministrador]

    def get_queryset(self):
        queryset = Usuario.objects.filter(rol__nombre='paciente')
        prioridad = self.request.query_params.get('prioridad', None)
        if prioridad:
            queryset = queryset.filter(usuarioinformacionpersonal__triage=prioridad)
        return queryset
    
class DetalleUsuarioView(generics.RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioDetalleSerializer
    permission_classes = [IsAdministrador]
    lookup_field = 'id'  # Puedes cambiar a otro campo si lo prefieres

class DetalleUsuarioDocumentoView(generics.RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioDetalleSerializer
    permission_classes = [IsAdministrador]
    lookup_field = 'id_documento'  # Puedes cambiar a otro campo si lo prefieres