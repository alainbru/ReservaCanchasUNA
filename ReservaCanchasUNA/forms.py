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