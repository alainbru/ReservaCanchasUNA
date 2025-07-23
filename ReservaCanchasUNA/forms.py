# ReservaCanchasUNA/forms.py

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Reserva, Persona

class Formulario_Persona(forms.Form):
    ROLES = [
        ('estudiante', 'Estudiante'),
        ('coordinador', 'Coordinador'),
        ('admin', 'Administrador'),
    ]
    CARRERAS = [
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
    # Modificación para permitir la edición sin cambiar el correo si no es necesario
    def clean_correo(self):
        correo = self.cleaned_data['correo']
        
        # Verificamos si estamos editando o creando
        if self.instance is not None:
            # Si estamos editando, verificamos si el correo ha cambiado
            if self.instance.correo == correo:
                return correo
        
        # Validación para correos institucionales
        if not correo.endswith('@est.unap.edu.pe'):
            raise ValidationError("Solo se permiten correos institucionales (@est.unap.edu.pe).")
        
        # Verificamos si el correo ya existe en la base de datos
        if Persona.objects.filter(correo=correo).exists():
            raise ValidationError("Este correo ya está registrado. Por favor, usa otro.")
        
        return correo

    escuela = forms.ChoiceField(choices=CARRERAS, label="Escuela Profesional")
    codigo = forms.IntegerField(
        required=True,
        label="Código",
        validators=[
            MinValueValidator(100000, message="El código debe tener 6 dígitos."),
            MaxValueValidator(999999, message="El código debe tener 6 dígitos.")
        ]
    )
    # Modificación para permitir la edición sin cambiar el código si no es necesario
    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        
        # Verificamos si estamos editando o creando
        if self.instance is not None:
            # Si estamos editando, verificamos si el código ha cambiado
            if self.instance.codigo == codigo:
                return codigo
        
        # Validación para verificar si el código ya existe en la base de datos
        if Persona.objects.filter(codigo=codigo).exists():
            raise ValidationError("Este código ya está registrado. Por favor, usa uno diferente.")
        
        return codigo

    contrasena = forms.CharField(max_length=100, widget=forms.PasswordInput, required=False, label="Contraseña")
    rol = forms.ChoiceField(choices=ROLES, label="Rol")

    # Constructor para inicializar el formulario con una instancia de Persona
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['nombre'].initial = self.instance.nombre
            self.fields['apellido_paterno'].initial = self.instance.apellido_paterno
            self.fields['apellido_materno'].initial = self.instance.apellido_materno
            self.fields['correo'].initial = self.instance.correo
            self.fields['escuela'].initial = self.instance.escuela
            self.fields['codigo'].initial = self.instance.codigo
            self.fields['rol'].initial = self.instance.rol
            # No inicializamos la contraseña por seguridad

class Formulario_Login(forms.Form):
    codigo = forms.IntegerField(
        required=True,
        label="Código",
        validators=[
            MinValueValidator(100000),
            MaxValueValidator(999999)
        ]
    )
    contrasena = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['dia', 'hora', 'cancha', 'deporte', 'disponible'] # Agregamos 'cancha' y 'deporte' para poder agregar reservas

# Nuevo formulario para Penalizaciones
class PenalizacionForm(forms.ModelForm):
     class Meta:
        model = Persona
        fields = ['penalizado', 'penalizacion_motivo'] # Añade 'penalizacion_motivo' aquí
        widgets = {
             'penalizacion_motivo': forms.Textarea(attrs={'rows': 4}), # Opcional: hazlo un área de texto
        }

