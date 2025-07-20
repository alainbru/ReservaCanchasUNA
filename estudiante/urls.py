from django.contrib import admin
from django.urls import include, path
from estudiante import views
from ReservaCanchasUNA.views import vista_reservas

app_name = 'estudiante'


urlpatterns = [
    path('', views.inicio_es, name='inicio_estudiante'),
    path('reservas/', vista_reservas, name='estudiante_reservas'),
    
    
    

]
