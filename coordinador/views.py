from django.shortcuts import render

# Create your views here.
def inicio_cor(request):
    return render(request, 'coordinador/inicio_cordinador.html')

from django.shortcuts import render, redirect
from .models import Reserva

from django.shortcuts import render, redirect
from .models import Reserva

from django.shortcuts import render, redirect
from .models import Reserva # Asegúrate de que Reserva esté en models.py

# coordinador/views.py
from django.shortcuts import render, redirect
from .models import Reserva # Asegúrate de que Reserva esté en models.py

def reservas_coordinador(request):
    deporte = request.GET.get('deporte', 'voley') # Default es 'voley' según tu imagen

    if request.user.is_staff:
        if request.method == 'POST':
            accion = request.POST.get('accion')
            reserva_id = request.POST.get('id_reserva')

            if accion == 'cancelar' and reserva_id:
                try:
                    reserva = Reserva.objects.get(id=reserva_id)
                    reserva.disponible = False
                    reserva.save()
                except Reserva.DoesNotExist:
                    pass
            
            elif accion == 'confirmar':
                nombre_escuela_coordinador = request.user.username 
                reservas_a_confirmar = Reserva.objects.filter(disponible=False, deporte=deporte)
                
                for reserva in reservas_a_confirmar:
                    reserva.escuela = nombre_escuela_coordinador
                    reserva.save()
                
                return redirect(f"{request.path}?deporte={deporte}")

    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    horas = [
        "7:00-8:00", "8:00-9:00", "9:00-10:00", "10:00-11:00",
        "11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00",
        "15:00-16:00", "16:00-17:00", "16:00-17:00", "17:00-18:00", "18:00-19:00", "19:00-20:00"
    ]
    
    # Asegúrate que estas listas de horas estén bien definidas y completas en tu views.py
    # Hay un error de copiado en tu ejemplo (16:00-17:00 repetido). Asegúrate que sea así:
    horas = [
        "7:00-8:00", "8:00-9:00", "9:00-10:00", "10:00-11:00",
        "11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00",
        "15:00-16:00", "16:00-17:00", "17:00-18:00", "18:00-19:00", "19:00-20:00"
    ]


    canchas_para_deporte = ['cancha 1'] if deporte in ['futbol', 'futsal'] else ['cancha 1', 'cancha 2']

    todas_las_reservas = Reserva.objects.filter(deporte=deporte)

    reservas_map = {}
    for reserva in todas_las_reservas:
        reservas_map[(reserva.dia, reserva.hora, reserva.cancha)] = reserva
    
    # Debugging: Imprime esto en la consola del servidor para ver si se están cargando los datos
    print(f"Deporte seleccionado: {deporte}")
    print(f"Días: {dias}")
    print(f"Horas: {horas}")
    print(f"Canchas para este deporte: {canchas_para_deporte}")
    print(f"Reservas cargadas (número): {len(todas_las_reservas)}")
    print(f"Contenido de reservas_map (ejemplo, las 5 primeras): {list(reservas_map.items())[:5]}")


    return render(request, 'coordinador/inicio_cordinador.html', {
        'dias': dias,
        'horas': horas,
        'canchas_para_deporte': canchas_para_deporte,
        'reservas_map': reservas_map,
        'deporte': deporte,
    })