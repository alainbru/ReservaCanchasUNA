from django.http import HttpResponse
from django.shortcuts import render
from . import forms, models
from ReservaCanchasUNA import views
from .models import Persona
from django.shortcuts import render
from .models import Persona
from django.http import HttpResponse



#---------------------------------------pagina por defecto---------------------------------------
def Index(request):
    return HttpResponse("esta funcioanndao correctaente ")

#---------------------------------------para registrar---------------------------------------
def crear_persona(request):
    if request.method == "POST":
        formulario = forms.Formulario_Persona(request.POST)
        if formulario.is_valid():
            nombres = formulario.cleaned_data['nombre']
            apellidop = formulario.cleaned_data['apellido_paterno']
            apellidom = formulario.cleaned_data['apellido_materno']
            correos = formulario.cleaned_data['correo']
            escuelas = formulario.cleaned_data['escuela']
            codigos = formulario.cleaned_data['codigo']
            contrasenas = formulario.cleaned_data['contrasena']
            rols = formulario.cleaned_data['rol']


            persona = models.Persona.objects.create(
                nombre=nombres,
                apellido_paterno=apellidop,
                apellido_materno=apellidom,
                correo=correos,
                escuela=escuelas,
                codigo=codigos,
                contrasena=contrasenas,
                rol=rols
            )
            return HttpResponse(f"Hola {nombres} {apellidop}, fuiste registrado correctamente.")

    else:
        formulario = forms.Formulario_Persona()
    return render(request, "ReservaCanchasUNA/persona.html", {"formulario": formulario})


def listar_personas(request):
    return render(request, "ReservaCanchasUNA/lista_personas.html",{"personas":models.Persona.objects.all()})
    