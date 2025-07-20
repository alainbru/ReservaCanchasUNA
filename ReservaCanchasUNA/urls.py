
from django.contrib import admin
from django.urls import path, include

from django.urls import path
from . import views


urlpatterns = [
    ##path('admin/ admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('registro/',views.registro, name='registro'),
    path('crear_persona/', views.crear_persona, name='crear_persona'),

]
