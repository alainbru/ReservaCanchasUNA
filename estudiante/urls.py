from django.contrib import admin
from django.urls import include, path
from estudiante import views

app_name = 'estudiante'


urlpatterns = [
    path('', views.inicio_es, name='inicio_estudiante'),

]
