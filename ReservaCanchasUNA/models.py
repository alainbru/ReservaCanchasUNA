from django.db import models

# Create your models here.
class Persona(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=100, blank=True, null=True)
    apellido_materno = models.CharField(max_length=100, blank=True, null=True)  
    correo = models.EmailField(max_length=100, blank=True, null=True)
    escuela = models.CharField(max_length=100, blank=True, null=True)
    codigo = models.CharField(max_length=100, blank=True, null=True)
    contrasena = models.CharField(max_length=100, blank=True, null=True)
    rol = models.CharField(max_length=100, blank=True, null=True)