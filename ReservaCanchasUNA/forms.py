from django import forms

class Formulario_Persona(forms.Form):
    nombre = forms.CharField(max_length=100, label="Nombre")
    apellidos = forms.CharField(max_length=100, label="Apellidos")