from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator

# Create your models here.
class Persona(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=100, blank=True, null=True)
    apellido_materno = models.CharField(max_length=100, blank=True, null=True)  
    correo = models.EmailField(max_length=100, unique=True, blank=True, null=True)
    escuela = models.CharField(max_length=100, blank=True, null=True)
    codigo = models.IntegerField( unique=True,
        blank=True, # Considera cambiar a False si siempre debe ser obligatorio
        null=True,  # Considera cambiar a False si siempre debe ser obligatorio
        validators=[
            MinValueValidator(100000, message="El código debe tener 6 dígitos."),
            MaxValueValidator(999999, message="El código debe tener 6 dígitos.")
        ]
    )
    contrasena = models.CharField(max_length=100, blank=True, null=True)
    rol = models.CharField(max_length=100, default='estudiante', null=False)
    penalizado = models.BooleanField(default=False)
    penalizacion_motivo = models.TextField(blank=True, null=True)
    # NUEVO CAMPO: Para la fecha y hora de la reserva (útil para auditoría y orden)
    fecha_reserva = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} ({self.rol})"


class Reserva(models.Model):
    dia = models.CharField(max_length=9)
    hora = models.CharField(max_length=20)
    cancha = models.CharField(max_length=20, blank=True, null=True)
    deporte = models.CharField(max_length=20, default='voley')
    disponible = models.BooleanField(default=None)
    persona = models.ForeignKey('Persona', null=True, blank=True, on_delete=models.SET_NULL)  # Nueva relación

    # NUEVO CAMPO: Para saber quién reservó la cancha
    reservado_por = models.ForeignKey(
        'Persona',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mis_reservas'
    )
    # NUEVO CAMPO: Para la fecha y hora de la reserva (útil para auditoría y orden)
    fecha_reserva = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return f"{self.deporte} - {self.dia} {self.hora} ({self.cancha if self.cancha else 'Cancha Única'}) - {'Disponible' if self.disponible else 'Reservado'}"
    cancelacion_confirmada = models.BooleanField(default=False)
