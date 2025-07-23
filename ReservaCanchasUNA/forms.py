from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Reserva, Persona
class Formulario_Persona(forms.Form):
    ROLES_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('coordinador', 'Coordinador'),
        ('admin', 'Administrador'),
    ]
    CARRERAS_CHOICES = [
        ('agronomia', 'Agronomía'),
        ('antropologia', 'Antropología'),
        ('arquitectura', 'Arquitectura y Urbanismo'),
        ('biologia', 'Biología'),
        ('ciencias_contables', 'Ciencias Contables'),
        ('ciencias_comunicacion', 'Ciencias de la Comunicación Social'),
        ('ciencias_fisicas_matematicas', 'Ciencias Físicas y Matemáticas'),
        ('ciencias_juridicas_politicas', 'Ciencias Jurídicas y Políticas'),
        ('ciencias_sociales', 'Ciencias Sociales'),
        ('educacion_inicial', 'Educación Inicial'),
        ('educacion_primaria', 'Educación Primaria'),
        ('educacion_secundaria', 'Educación Secundaria'),
        ('enfermeria', 'Enfermería'),
        ('estadistica_informatica', 'Estadística e Informática'),
        ('farmacia_bioquimica', 'Farmacia y Bioquímica'),
        ('ingenieria_agricola', 'Ingeniería Agrícola'),
        ('ingenieria_agroindustrial', 'Ingeniería Agroindustrial'),
        ('ingenieria_civil', 'Ingeniería Civil'),
        ('ingenieria_electronica', 'Ingeniería Electrónica'),
        ('ingenieria_estadistica', 'Ingeniería Estadística'),
        ('ingenieria_geologica', 'Ingeniería Geológica'),
        ('ingenieria_minas', 'Ingeniería de Minas'),
        ('ingenieria_metalurgica', 'Ingeniería Metalúrgica'),
        ('ingenieria_quimica', 'Ingeniería Química'),
        ('ingenieria_sistemas', 'Ingeniería de Sistemas'),
        ('medicina_humana', 'Medicina Humana'),
        ('medicina_veterinaria', 'Medicina Veterinaria y Zootecnia'),
        ('nutricion_humana', 'Nutrición Humana'),
        ('odontologia', 'Odontología'),
        ('psicologia', 'Psicología'),
        ('sociologia', 'Sociología'),
        ('turismo', 'Turismo'),
        # Puedes añadir más carreras aquí
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
    # Validación de dominio institucional
        if not correo.endswith('@est.unap.edu.pe'):
            raise ValidationError("Solo se permiten correos institucionales (@est.unap.edu.pe).")
    # Validación de unicidad
        if Persona.objects.filter(correo=correo).exists():
            raise ValidationError("Este correo ya está registrado. Por favor, usa otro.")
        return correo
    escuela = forms.ChoiceField(choices=CARRERAS_CHOICES, label="Escuela Profesional")
    codigo = forms.IntegerField(
        required=True, # Considera cambiar a True si siempre debe ser obligatorio
        label="Código",
        validators=[
            MinValueValidator(100000, message="El código debe tener 6 dígitos."),
            MaxValueValidator(999999, message="El código debe tener 6 dígitos.")
        ]
    )
    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        if Persona.objects.filter(codigo=codigo).exists():
            raise ValidationError("Este código ya está registrado. Por favor, usa uno diferente.")
        return codigo
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
