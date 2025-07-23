from django.contrib import admin
from django.urls import include, path
from estudiante import views
from ReservaCanchasUNA.views import vista_reservas

app_name = 'estudiante'


urlpatterns = [
    path('', views.inicio_es, name='inicio_estudiante'),
    
    path('reservas_es/', views.reservas_es, name='reservas_es'),
    
    
    

]
