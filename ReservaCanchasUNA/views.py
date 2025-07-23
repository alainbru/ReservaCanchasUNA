from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

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
    if request.method == 'POST':
        reserva_id = request.POST.get('id_reserva')
        # No necesitamos 'accion' aquí si esta vista es solo para que el estudiante reserve
        reserva = get_object_or_404(Reserva, id=reserva_id)
        # Asumiendo que el usuario logueado es una Persona y está en request.session['persona_id']
        # Si usas el sistema de autenticación de Django, adapta esto a request.user.persona
        if 'persona_id' in request.session:
            persona_logueada = get_object_or_404(Persona, id=request.session['persona_id'])
            if persona_logueada.rol == 'estudiante': # Asegurarse que solo estudiantes puedan reservar aquí
                if reserva.disponible:
                    reserva.disponible = False
                    reserva.reservado_por = persona_logueada # Asigna la persona logueada
                    reserva.fecha_reserva = timezone.now() # Registra la fecha y hora de la reserva
                    reserva.save()
                    messages.success(request, '¡Reserva realizada con éxito!')
                else:
                    messages.error(request, 'Esta franja ya no está disponible.')
            else:
                messages.error(request, 'Solo los estudiantes pueden realizar reservas desde aquí.')
        else:
            messages.error(request, 'Debes iniciar sesión para reservar.')
        return redirect(f"{request.path}?deporte={deporte}")
    # Lógica para mostrar el calendario (GET request)
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    horas = [
        "7:00-8:00", "8:00-9:00", "9:00-10:00", "10:00-11:00",
        "11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00",
        "15:00-16:00", "16:00-17:00", "17:00-18:00", "18:00-19:00", "19:00-20:00"
    ]
    # Obtener todas las reservas para el deporte seleccionado
    if deporte != 'futbol':
        canchas = ['cancha 1', 'cancha 2']
        # Usamos .all() y luego filtramos en la plantilla para simplificar la vista
        reservas_queryset = Reserva.objects.filter(deporte=deporte).select_related('reservado_por')
    else:
        canchas = []
        reservas_queryset = Reserva.objects.filter(deporte=deporte).select_related('reservado_por')
    return render(request, 'ReservaCanchasUNA/reservas.html', {
        'dias': dias,
        'horas': horas,
        'canchas': canchas,
        'reservas_queryset': reservas_queryset, # Pasamos el queryset completo
        'deporte': deporte,
    })
