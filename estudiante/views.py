from django.shortcuts import redirect, render
from ReservaCanchasUNA.models import Reserva

# Create your views here.
def inicio_es(request):
    return render(request, 'estudiante/inicio_estudiante.html')


def reservas_es(request):
    deporte = request.GET.get('deporte', 'futbol')  # Default is fútbol

    # Verifica si ya reservó en la sesión
    ya_reservo = request.session.get(f'reservo_{deporte}', False)

    if request.method == 'POST' and not ya_reservo:
        reserva_id = request.POST.get('id_reserva')
        reserva = Reserva.objects.get(id=reserva_id)
        reserva.disponible = False
        reserva.save()
        # Marca que ya reservó en la sesión
        request.session[f'reservo_{deporte}'] = True
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
        'ya_reservo': ya_reservo,
    })
