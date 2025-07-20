from django.http import HttpResponse
from django.shortcuts import render
from . import forms, models
from ReservaCanchasUNA import views
from .models import Persona
from django.shortcuts import render
from .models import Persona
from django.http import HttpResponse

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Reserva

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
    
#'''---------------------------------------para reservas---------------------------------------
def vista_reservas(request):
    deporte = request.GET.get('deporte', 'futbol')  # por defecto muestra fútbol

    if request.method == 'POST':
        reserva_id = request.POST.get('id_reserva')
        reserva = Reserva.objects.get(id=reserva_id)
        reserva.disponible = False
        reserva.save()
        return redirect(f"{request.path}?deporte={deporte}")  # mantiene el deporte seleccionado

    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    horas = [
        "7:00-8:00", "8:00-9:00", "9:00-10:00", "10:00-11:00",
        "11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00",
        "15:00-16:00", "16:00-17:00", "17:00-18:00", "18:00-19:00", "19:00-20:00"
    ]

    canchas = ['cancha 1', 'cancha 2'] if deporte != 'futbol' else ['']
    reservas = Reserva.objects.filter(deporte=deporte)

    return render(request, 'ReservaCanchasUNA/reservas.html', {
        'dias': dias,
        'horas': horas,
        'canchas': canchas,
        'reservas': reservas,
        'deporte': deporte,
    })
