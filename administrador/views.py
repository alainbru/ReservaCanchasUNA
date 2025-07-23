# administrador/views.py

from django.shortcuts import render,redirect, get_object_or_404
from ReservaCanchasUNA.models import Persona, Reserva #importamos la base desde el principal
from ReservaCanchasUNA.forms import Formulario_Persona, ReservaForm, PenalizacionForm # Importamos el formulario de Persona y ReservaForm
from django.contrib import messages # Para mostrar mensajes al usuario

def inicio_ad(request):
    return render(request, 'administrador/inicio_admin.html')

def lista_usuarios(request):
    personas = Persona.objects.all()  # Traes todos los registros de Persona
    return render(request, 'administrador/lista_usuarios.html', {'personas': personas})

def eliminar_persona(request, persona_id):
    persona= get_object_or_404(Persona, id=persona_id)
    persona.delete()
    messages.success(request, 'Persona eliminada correctamente.') # Mensaje de éxito
    return redirect('admin:lista_usuarios')

def editar_persona(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)
    if request.method == 'POST':
        formulario = Formulario_Persona(request.POST, instance=persona) # Pasamos la instancia para editar
        if formulario.is_valid():
            # Actualizamos los campos de la persona
            persona.nombre = formulario.cleaned_data['nombre']
            persona.apellido_paterno = formulario.cleaned_data['apellido_paterno']
            persona.apellido_materno = formulario.cleaned_data['apellido_materno']
            persona.correo = formulario.cleaned_data['correo']
            persona.escuela = formulario.cleaned_data['escuela']
            persona.codigo = formulario.cleaned_data['codigo']
            # Solo actualizamos la contraseña si se proporciona una nueva
            if formulario.cleaned_data['contrasena']:
                persona.contrasena = formulario.cleaned_data['contrasena']
            persona.rol = formulario.cleaned_data['rol']
            persona.save()
            messages.success(request, 'Persona actualizada correctamente.')
            return redirect('admin:lista_usuarios')
    else:
        formulario = Formulario_Persona(instance=persona) # Inicializamos el formulario con los datos de la persona
    return render(request, 'administrador/editar_persona.html', {'formulario': formulario, 'persona': persona})

# Funciones para la gestión de reservas (se añadirán más adelante)

from django.shortcuts import render, redirect, get_object_or_404
from ReservaCanchasUNA.models import Persona, Reserva
from ReservaCanchasUNA.forms import ReservaForm # Solo necesitamos ReservaForm aquí
from django.contrib import messages
from django.utils import timezone

# ... (otras funciones existentes)

def gestionar_reservas_admin(request):
    if request.method == 'POST':
        deporte = request.POST.get('deporte', 'futbol') # Obtener del POST, si no está, default a 'futbol'
    else:
        deporte = request.GET.get('deporte', 'futbol') # Obtener del GET, si no está, default a 'futbol'
    # Lógica para acciones POST del administrador
    if request.method == 'POST':
        accion = request.POST.get('accion')
        reserva_id = request.POST.get('id_reserva')

        if accion == 'eliminar_individual':
            reserva = get_object_or_404(Reserva, id=reserva_id)
            reserva.delete()
            messages.success(request, 'Reserva eliminada individualmente.')
        elif accion == 'liberar_individual':
            reserva = get_object_or_404(Reserva, id=reserva_id)
            reserva.disponible = True
            reserva.reservado_por = None
            reserva.fecha_reserva = None
            reserva.save()
            messages.success(request, 'Reserva liberada correctamente.')
        elif accion == 'eliminar_todas':
            Reserva.objects.all().delete()
            messages.success(request, 'Todas las reservas han sido eliminadas.')
        elif accion == 'agregar_reserva_manual':
            # Para agregar manualmente desde el botón "Agregar" en la celda
            dia = request.POST.get('dia')
            hora = request.POST.get('hora')
            cancha = request.POST.get('cancha') # Será None para fútbol
            deporte_post = request.POST.get('deporte') # Deporte actual del filtro
            disponible = request.POST.get('disponible') == 'True' # Convertir a booleano

            # Crear la reserva directamente
            Reserva.objects.create(
                dia=dia,
                hora=hora,
                cancha=cancha if cancha != 'None' else None, # Asegurar que 'None' de HTML sea None de Python
                deporte=deporte_post,
                disponible=disponible
            )
            messages.success(request, 'Reserva agregada manualmente.')

        return redirect(f"{request.path}?deporte={deporte}") # Redirige a la misma página con el deporte actual

    # Lógica para mostrar el calendario (GET request)
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    horas = [
        "7:00-8:00", "8:00-9:00", "9:00-10:00", "10:00-11:00",
        "11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00",
        "15:00-16:00", "16:00-17:00", "17:00-18:00", "18:00-19:00", "19:00-20:00"
    ]

    # Obtener todas las reservas para el deporte seleccionado
    reservas_queryset = Reserva.objects.filter(deporte=deporte).select_related('reservado_por')

    # Preparar los datos para la plantilla de una manera que no necesite el filtro
    # Creamos una estructura de datos que la plantilla pueda iterar directamente
    calendario_reservas = []
    for hora in horas:
        fila_hora = {'hora': hora, 'dias': []}
        for dia in dias:
            celda_dia = {'dia': dia, 'canchas': []}
            
            # Para deportes con canchas múltiples
            if deporte != 'futbol':
                canchas_nombres = ['cancha 1', 'cancha 2']
                for cancha_nombre in canchas_nombres:
                    # Buscar la reserva específica para esta celda
                    reserva_encontrada = None
                    for res in reservas_queryset:
                        if res.dia == dia and res.hora == hora and res.cancha == cancha_nombre:
                            reserva_encontrada = res
                            break # Encontrada, salir del bucle interno
                    celda_dia['canchas'].append({'nombre': cancha_nombre, 'reserva': reserva_encontrada})
            else: # Para fútbol, solo una "cancha" por franja
                reserva_encontrada = None
                for res in reservas_queryset:
                    if res.dia == dia and res.hora == hora:
                        reserva_encontrada = res
                        break
                celda_dia['canchas'].append({'nombre': 'unica', 'reserva': reserva_encontrada}) # 'unica' es solo un marcador

            fila_hora['dias'].append(celda_dia)
        calendario_reservas.append(fila_hora)

    return render(request, 'administrador/gestionar_reservas_admin.html', {
        'dias': dias,
        'horas': horas,
        'deporte': deporte,
        'calendario_reservas': calendario_reservas, # Pasamos la estructura preparada
    })



# Funciones para la gestión de penalizaciones (se añadirán más adelante)
from ReservaCanchasUNA.forms import PenalizacionForm # Importar el formulario de penalización

def gestionar_penalizaciones(request):
    # Asumimos que Persona tiene un campo 'penalizado'
    personas_penalizadas = Persona.objects.filter(penalizado=True)
    return render(request, 'administrador/gestionar_penalizaciones.html', {'personas_penalizadas': personas_penalizadas})
def penalizar_usuario(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)
    if request.method == 'POST':
        form = PenalizacionForm(request.POST, instance=persona) # Usa PenalizacionForm
        if form.is_valid():
            persona.penalizado = True # Asegura que penalizado se establezca en True
            persona.penalizacion_motivo = form.cleaned_data['penalizacion_motivo'] # Obtiene el motivo
            persona.save()
            messages.success(request, f'Usuario {persona.nombre} penalizado correctamente.')
            return redirect('admin:gestionar_penalizaciones')
    else:
        form = PenalizacionForm(instance=persona) # Pasa la instancia para prellenar si es necesario
    return render(request, 'administrador/confirmar_penalizacion.html', {'persona': persona, 'form': form}) # Pasa el formulario a la plantilla
def quitar_penalizacion(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)
    if request.method == 'POST':
        persona.penalizado = False # Quitar penalización
        persona.penalizacion_motivo = None # Limpiar el motivo al despenalizar
        persona.save()
        messages.success(request, f'Penalización quitada a {persona.nombre} correctamente.')
        return redirect('admin:gestionar_penalizaciones')
    return render(request, 'administrador/confirmar_quitar_penalizacion.html', {'persona': persona})


