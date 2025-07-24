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
            # Redirige al usuario a la página de login después de un registro exitoso
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('login_view') # Asumiendo que 'login_view' es el nombre de tu URL de login

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
                # Guardar el correo en la sesión para el estudiante
                request.session['correo'] = persona.correo 
                
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
    persona_id = request.session.get('persona_id')
    rol = None
    if persona_id:
        persona = Persona.objects.get(id=persona_id)
        rol = persona.rol

    deporte = request.GET.get('deporte', 'futbol')

    # Verifica si el estado ya es permanente
    cancelacion_permanente = Reserva.objects.filter(cancelacion_confirmada=True).exists()

    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'confirmar_cancelacion' and not cancelacion_permanente:
            # Guardar el estado permanente en la BD
            Reserva.objects.all().update(cancelacion_confirmada=True)
            messages.success(request, 'Todas las cancelaciones han sido confirmadas permanentemente.')
        elif accion == 'cancelar' and not cancelacion_permanente:
            reserva_id = request.POST.get('id_reserva')
            reserva = get_object_or_404(Reserva, id=reserva_id)
            reserva.disponible = False
            reserva.save()
            messages.info(request, f'Reserva {reserva.dia} {reserva.hora} marcada como no disponible.')
        elif accion == 'confirmar' and not cancelacion_permanente:
            reserva_id = request.POST.get('id_reserva')
            reserva = get_object_or_404(Reserva, id=reserva_id)
            reserva.disponible = True
            reserva.save()
            messages.success(request, f'Reserva {reserva.dia} {reserva.hora} marcada como disponible.')
        return redirect(f"{request.path}?deporte={deporte}")

    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    horas = [
        "7:00-8:00", "8:00-9:00", "9:00-10:00", "10:00-11:00",
        "11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00",
        "15:00-16:00", "16:00-17:00", "17:00-18:00", "18:00-19:00", "19:00-20:00"
    ]
    
    # Aseguramos que 'reservas_queryset' siempre se defina
    if deporte != 'futbol':
        canchas = ['cancha 1', 'cancha 2']
        reservas_queryset = Reserva.objects.filter(deporte=deporte).select_related('reservado_por')
    else:
        canchas = []
        # CAMBIO AQUÍ: Renombramos 'reservas' a 'reservas_queryset'
        reservas_queryset = Reserva.objects.filter(deporte=deporte, dia__in=dias, hora__in=horas)

    return render(request, 'ReservaCanchasUNA/reservas.html', {
        'dias': dias,
        'horas': horas,
        'canchas': canchas,
        'reservas': reservas_queryset, # Usamos 'reservas' para que coincida con la plantilla 'reservas.html'
                                      # que itera sobre 'reservas'
        'deporte': deporte,
        'cancelacion_confirmada': cancelacion_permanente,
        'rol': rol,
    })

