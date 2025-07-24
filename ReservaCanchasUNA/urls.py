"""
URL configuration for ReservaCanchasUNA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from ReservaCanchasUNA import views
from django.conf.urls.static import static


urlpatterns = [
    
    path('', views.principal, name='principal'),

    path('', views.inicio, name='inicio'),
    
    path('crearpersona/', views.crear_persona, name='crear_persona'),
    path('listarpersona/', views.listar_personas, name='listar_personas'),
    
    path('login/', views.login_view, name='login_view'),
    
    ##para redicionar a los aps
    path('administrador/', include('administrador.urls',namespace='admin')),
    path('estudiante/', include('estudiante.urls',namespace='estudiante')),
    path('coordinador/', include('coordinador.urls',namespace='coordinador')), 

    ######faltaria solucionar bien esa
    #path('reservas/', views.vista_reservas, name='vista_reservas'),
    #solucionar la parte de longin y registro 
]
