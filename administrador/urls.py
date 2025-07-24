# administrador/urls.py

from django.contrib import admin
from django.urls import path
from administrador import views

app_name = 'admin'
urlpatterns = [
    path('', views.inicio_ad, name='inicio_admin'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/eliminar/<int:persona_id>/', views.eliminar_persona, name='eliminar_persona'),
    path('usuarios/editar/<int:persona_id>/', views.editar_persona, name='editar_persona'),
    # URLs para la gestión de reservas (AHORA APUNTAN A LA NUEVA VISTA)
    path('reservas/', views.gestionar_reservas_admin, name='gestionar_reservas'),
    # URLs para la gestión de penalizaciones
    path('penalizaciones/penalizar/<int:persona_id>/', views.penalizar_usuario, name='penalizar_usuario'),
    path('penalizaciones/', views.gestionar_penalizaciones, name='gestionar_penalizaciones'),
    path('penalizaciones/quitar/<int:persona_id>/', views.quitar_penalizacion, name='quitar_penalizacion'),
]
