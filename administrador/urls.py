
from django.contrib import admin
from django.urls import path
from administrador import views

app_name = 'admin'

urlpatterns = [
    path('', views.inicio_ad, name='inicio_admin'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    
    ##Un boton para eliminar a una persona
    path('usuarios/eliminar/<int:persona_id>/', views.eliminar_persona, name='eliminar_persona'),

    
]
