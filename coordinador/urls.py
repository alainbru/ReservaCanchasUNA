from django.contrib import admin
from django.urls import include, path
from coordinador import views
from ReservaCanchasUNA.views import vista_reservas


app_name = 'coordinador'


urlpatterns = [
    path('', views.inicio_cor, name='inicio_coordinador'),
    path('reservas/', vista_reservas, name='coordinador_reservas'),


]
