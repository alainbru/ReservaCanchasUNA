from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

class Formulario_Persona(forms.Form):
    ROLES_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('coordinador', 'Coordinador'),
        ('admin', 'Administrador'),
    ]
    nombre = forms.CharField(max_length=100, label="Nombre")
    apellido_paterno = forms.CharField(max_length=100, label="Apellido Paterno")
    apellido_materno = forms.CharField(max_length=100, label="Apellido Materno")
    correo = forms.EmailField(
        label="Correo Institucional",
        help_text="Debe ser un correo @est.unap.edu.pe"
    )
    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if not correo.endswith('@est.unap.edu.pe'):
            raise ValidationError("Solo se permiten correos de la UNA DNI(@est.unap.edu.pe)")
        return correo
    escuela = forms.CharField(max_length=100, required=False, label="Escuela")
    codigo = forms.IntegerField(
        required=True, 
        label="Código",
        validators=[
            MinValueValidator(100000, message="El código debe tener 6 dígitos."),
            MaxValueValidator(999999, message="El código debe tener 6 dígitos.")
        ]
    )
    contrasena = forms.CharField(max_length=100, widget=forms.PasswordInput, required=False, label="Contraseña")
    rol = forms.ChoiceField(choices=ROLES_CHOICES, label="Rol")
    
class Formulario_Login(forms.Form):
    codigo = forms.CharField(label="Codigo")
    contrasena = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['dia', 'hora', 'disponible']
