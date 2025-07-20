from django.contrib import admin
from django.urls import include, path
from coordinador import views

app_name = 'coordinador'


urlpatterns = [
    path('', views.inicio_cor, name='inicio_coordinador'),

]
