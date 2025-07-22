from django.db import models
from ReservaCanchasUNA.models import Reserva

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Reserva(models.Model):
    deporte = models.CharField(max_length=50)
    dia = models.CharField(max_length=20)
    hora = models.CharField(max_length=20)
    cancha = models.CharField(max_length=20)
    disponible = models.BooleanField(default=True) # True = disponible, False = cancelada por coordinador o reservada por estudiante
    escuela = models.CharField(max_length=100, blank=True, null=True) # Para guardar el nombre de la escuela/coordinador

    def __str__(self):
        return f"{self.deporte} - {self.dia} {self.hora} en {self.cancha}"

    class Meta:
        unique_together = ('deporte', 'dia', 'hora', 'cancha') # Para evitar duplicados de reservas