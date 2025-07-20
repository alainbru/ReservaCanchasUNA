from django import forms

class Formulario_Persona(forms.Form):
    nombre = forms.CharField(max_length=100, label="Nombre")
    apellido_paterno = forms.CharField(max_length=100, label="Apellido Paterno")
    apellido_materno = forms.CharField(max_length=100, label="Apellido Materno")
    correo= forms.EmailField(max_length=100, required=False, label="Correo Electrónico")
    escuela = forms.CharField(max_length=100, required=False, label="Escuela")
    codigo = forms.CharField(max_length=100, required=False, label="Código")
    contrasena = forms.CharField(max_length=100, widget=forms.PasswordInput, required=False, label="Contraseña")
    rol = forms.CharField(max_length=100, required=False, label="Rol")
    
class Formulario_Login(forms.Form):
    correo = forms.EmailField(label="Usuario")
    contrasena = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['dia', 'hora', 'disponible']
