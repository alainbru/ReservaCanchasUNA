from django.shortcuts import redirect, render
from ReservaCanchasUNA.models import Reserva, Persona

# Create your views here.
def inicio_es(request):
    return render(request, 'estudiante/inicio_estudiante.html')


def reservas_es(request):
    deporte = request.GET.get('deporte', 'futbol')
    correo = request.session.get('correo')  # Debes guardar el correo en sesión al iniciar sesión
    persona = Persona.objects.filter(correo=correo).first()

    cantidad_reservas = Reserva.objects.filter(deporte=deporte, persona=persona, disponible=False).count()

    if request.method == 'POST' and cantidad_reservas <= 2:
        reserva_id = request.POST.get('id_reserva')
        reserva = Reserva.objects.get(id=reserva_id)

        reserva.disponible = False
        reserva.persona = persona
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
        # Filtrar reservas para el deporte y canchas específicas
        reservas = Reserva.objects.filter(deporte=deporte, dia__in=dias, hora__in=horas, cancha__in=canchas)
    else:
        canchas = []  # Para fútbol, no hay canchas separadas en la tabla
        # Filtrar reservas para el deporte (fútbol)
        reservas = Reserva.objects.filter(deporte=deporte, dia__in=dias, hora__in=horas)

    return render(request, 'estudiante/reservas_es.html', {
        'dias': dias,
        'horas': horas,
        'canchas': canchas,
        'reservas': reservas,
        'deporte': deporte,
        'ya_reservo': cantidad_reservas >= 2,  # Verifica si ya hizo 2 reservas
    })