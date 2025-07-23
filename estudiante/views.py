from django.shortcuts import redirect, render
from ReservaCanchasUNA.models import Reserva

# Create your views here.
def inicio_es(request):
    return render(request, 'estudiante/inicio_estudiante.html')


def reservas_es(request):
    deporte = request.GET.get('deporte', 'futbol')  # Default is fútbol

    if request.method == 'POST':
        reserva_id = request.POST.get('id_reserva')
        reserva = Reserva.objects.get(id=reserva_id)
        reserva.disponible = False
        reserva.save()
        return redirect(f"{request.path}?deporte={deporte}")  # Keep the selected sport

    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    horas = [
        "7:00-8:00", "8:00-9:00", "9:00-10:00", "10:00-11:00",
        "11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00",
        "15:00-16:00", "16:00-17:00", "17:00-18:00", "18:00-19:00", "19:00-20:00"
    ]

    # For non-football sports, include both "cancha 1" and "cancha 2"
    if deporte != 'futbol':
        canchas = ['cancha 1', 'cancha 2']
        reservas = Reserva.objects.filter(deporte=deporte, dia__in=dias, hora__in=horas, cancha__in=canchas)
    else:
        canchas = []
        reservas = Reserva.objects.filter(deporte=deporte, dia__in=dias, hora__in=horas)


    return render(request, 'estudiante/reservas_es.html', {
        'dias': dias,
        'horas': horas,
        'canchas': canchas,
        'reservas': reservas,
        'deporte': deporte,
    })
