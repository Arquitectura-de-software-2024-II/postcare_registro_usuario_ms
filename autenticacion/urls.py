from django.urls import path

from .views import(
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    LogoutView,
    UpdateUserInfoView,
    UserFormInfoView,
    CustomUserViewSet,
    ListaPacientesView,
    DetalleUsuarioView,
    DetalleUsuarioDocumentoView
)

urlpatterns = [
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path('jwt/logout/', LogoutView.as_view()),
    path('form-info/', UserFormInfoView.as_view()),
    path('update-info/', UpdateUserInfoView.as_view()),
    path('users/me/', CustomUserViewSet.as_view({'get': 'list'})),
    path('pacientes/', ListaPacientesView.as_view()),
    path('pacientes/<int:id>/', DetalleUsuarioView.as_view()),
    path('pacientes/documento/<str:id_documento>/', DetalleUsuarioDocumentoView.as_view())
]