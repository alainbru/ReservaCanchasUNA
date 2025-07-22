from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator

# Create your models here.
class Persona(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=100, blank=True, null=True)
    apellido_materno = models.CharField(max_length=100, blank=True, null=True)  
    correo = models.EmailField(max_length=100, blank=True, null=True)
    escuela = models.CharField(max_length=100, blank=True, null=True)
    codigo = models.IntegerField(
        blank=True, # Considera cambiar a False si siempre debe ser obligatorio
        null=True,  # Considera cambiar a False si siempre debe ser obligatorio
        validators=[
            MinValueValidator(100000, message="El código debe tener 6 dígitos."),
            MaxValueValidator(999999, message="El código debe tener 6 dígitos.")
        ]
    )
    contrasena = models.CharField(max_length=100, blank=True, null=True)
    rol = models.CharField(max_length=100, default='estudiante', null=False)
    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} ({self.rol})"


class Reserva(models.Model):
    dia = models.CharField(max_length=9)
    hora = models.CharField(max_length=20)
    cancha = models.CharField(max_length=20, blank=True, null=True)  # Solo para voley/basquet/futsal
    deporte = models.CharField(max_length=20, default='voley')  # ejemplo # voley, basquet, futsal, futbol
    disponible = models.BooleanField(default=True)
