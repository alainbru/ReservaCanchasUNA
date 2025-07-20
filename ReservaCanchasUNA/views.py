from django.shortcuts import redirect, render
from django.http import HttpResponse
import datetime
from . import forms, models


def inicio(request):
    return render(request, 'ReservaCanchasUNA/inicio.html')

def registro(request):
    return render(request, 'ReservaCanchasUNA/registrarse.html')

def registro(request):
    formulario = forms.Formulario_Persona()
    return render(request, 'ReservaCanchasUNA/registrarse.html', {
        "formulario": formulario
    })

##Para crear los registros
def crear_persona(request):
   
    if(request.method == "POST"):
        formulario = forms.Formulario_Persona(request.POST)
        if(formulario.is_valid()):
            nombres = formulario.cleaned_data['nombre']
            apellidos = formulario.cleaned_data['apellidos']
            persona = models.Persona.objects.create(nombre = nombres, apellidos = apellidos)
            persona.save()
            return HttpResponse("Hola " + nombres + " " + apellidos + ", fuiste registrado correctamente.")
            #return HttpResponse(models.Persona.objects.all())
    formulario = forms.Formulario_Persona()
    return render(request, 'ReservaCanchasUNA/registrarse.html', {
        "formulario": formulario
    })
