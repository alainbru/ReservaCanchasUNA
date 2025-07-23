from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from . import forms, models
from .forms import Formulario_Login
from .models import Persona
from .models import Reserva

#---------------------------------------Pagina princiapl---------------------------------------
def principal(request):
    return render(request, 'ReservaCanchasUNA/principal.html')

#---------------------------------------Pagina inicio---------------------------------------
def inicio(request):
    return render(request, 'ReservaCanchasUNA/inicio.html')



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
            return HttpResponse(f"Hola {nombres} {apellidop}, fuiste registrado correctamente." )     


    else:
        formulario = forms.Formulario_Persona()
    return render(request, "ReservaCanchasUNA/persona.html", {"formulario": formulario})


def listar_personas(request):
    return render(request, "ReservaCanchasUNA/lista_personas.html",{"personas":models.Persona.objects.all()})


#---------------------------------------para logiarse---------------------------------------
def login_view(request):
    if request.method == 'POST':
        form = Formulario_Login(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['codigo']
            contrasena = form.cleaned_data['contrasena']
            
            try:
                persona = Persona.objects.get(codigo=codigo, contrasena=contrasena)
                request.session['persona_id'] = persona.id
                
                if persona.rol == 'admin':
                    return redirect('admin:inicio_admin')
                if persona.rol == 'estudiante':
                    return redirect('estudiante:inicio_estudiante')
                if persona.rol == 'coordinador':
                    return redirect('coordinador:inicio_coordinador')
            
            except Persona.DoesNotExist:
                messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = Formulario_Login()
    
    return render(request, 'ReservaCanchasUNA/login.html', {'formulario': Formulario_Login()})
    
#'''---------------------------------------para reservas---------------------------------------
def vista_reservas(request):
    deporte = request.GET.get('deporte', 'futbol')
    cancelacion_confirmada = request.session.get('cancelacion_confirmada', False)

    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'confirmar_cancelacion':
            cancelacion_confirmada = True
            request.session['cancelacion_confirmada'] = True
        elif accion == 'cancelar':
            reserva_id = request.POST.get('id_reserva')
            reserva = Reserva.objects.get(id=reserva_id)
            reserva.disponible = False
            reserva.save()
        elif accion == 'confirmar':
            reserva_id = request.POST.get('id_reserva')
            reserva = Reserva.objects.get(id=reserva_id)
            reserva.disponible = True
            reserva.save()
        return redirect(f"{request.path}?deporte={deporte}")

    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    horas = [
        "7:00-8:00", "8:00-9:00", "9:00-10:00", "10:00-11:00",
        "11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00",
        "15:00-16:00", "16:00-17:00", "17:00-18:00", "18:00-19:00", "19:00-20:00"
    ]

    if deporte != 'futbol':
        canchas = ['cancha 1', 'cancha 2']
        reservas = Reserva.objects.filter(deporte=deporte, dia__in=dias, hora__in=horas, cancha__in=canchas)
    else:
        canchas = []
        reservas = Reserva.objects.filter(deporte=deporte, dia__in=dias, hora__in=horas)

    return render(request, 'ReservaCanchasUNA/reservas.html', {
        'dias': dias,
        'horas': horas,
        'canchas': canchas,
        'reservas': reservas,
        'deporte': deporte,
        'cancelacion_confirmada': cancelacion_confirmada,
    })