# administrador/urls.py

from django.contrib import admin
from django.urls import path
from administrador import views

app_name = 'admin'

urlpatterns = [
    path('', views.inicio_ad, name='inicio_admin'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    
    ##Un boton para eliminar a una persona
    path('usuarios/eliminar/<int:persona_id>/', views.eliminar_persona, name='eliminar_persona'),
    path('usuarios/editar/<int:persona_id>/', views.editar_persona, name='editar_persona'), # Nueva URL para editar

    # URLs para la gestión de reservas
    path('reservas/', views.gestionar_reservas, name='gestionar_reservas'),
    path('reservas/agregar/', views.agregar_reserva, name='agregar_reserva'),
    path('reservas/editar/<int:reserva_id>/', views.editar_reserva, name='editar_reserva'),
    path('reservas/eliminar/<int:reserva_id>/', views.eliminar_reserva, name='eliminar_reserva'),

    # URLs para la gestión de penalizaciones
    path('penalizaciones/', views.gestionar_penalizaciones, name='gestionar_penalizaciones'),
    path('penalizaciones/penalizar/<int:persona_id>/', views.penalizar_usuario, name='penalizar_usuario'),
    path('penalizaciones/quitar/<int:persona_id>/', views.quitar_penalizacion, name='quitar_penalizacion'),
]

