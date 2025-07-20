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


class Reserva(models.Model):
    dia = models.CharField(max_length=9)
    hora = models.CharField(max_length=20)
    cancha = models.CharField(max_length=20, blank=True, null=True)  # Solo para voley/basquet/futsal
    deporte = models.CharField(max_length=20, default='voley')  # ejemplo # voley, basquet, futsal, futbol
    disponible = models.BooleanField(default=True)
