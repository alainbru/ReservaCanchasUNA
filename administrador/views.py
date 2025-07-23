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
def gestionar_reservas(request):
    reservas = Reserva.objects.all().order_by('dia', 'hora', 'cancha')
    return render(request, 'administrador/gestionar_reservas.html', {'reservas': reservas})

def agregar_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva agregada correctamente.')
            return redirect('admin:gestionar_reservas')
    else:
        form = ReservaForm()
    return render(request, 'administrador/agregar_editar_reserva.html', {'form': form, 'accion': 'Agregar'})

def editar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva actualizada correctamente.')
            return redirect('admin:gestionar_reservas')
    else:
        form = ReservaForm(instance=reserva)
    return render(request, 'administrador/agregar_editar_reserva.html', {'form': form, 'accion': 'Editar'})

def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    reserva.delete()
    messages.success(request, 'Reserva eliminada correctamente.')
    return redirect('admin:gestionar_reservas')

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


