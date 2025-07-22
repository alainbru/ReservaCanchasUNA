from django.shortcuts import render,redirect, get_object_or_404
from ReservaCanchasUNA.models import Persona #importamos la base desde el principal

def inicio_ad(request):
    return render(request, 'administrador/inicio_admin.html')

def lista_usuarios(request):
    personas = Persona.objects.all()  # Traes todos los registros de Persona
    return render(request, 'administrador/lista_usuarios.html', {'personas': personas})


def eliminar_persona(request, persona_id):
    persona= get_object_or_404(Persona, id=persona_id)
    persona.delete()
    return redirect('admin:lista_usuarios')