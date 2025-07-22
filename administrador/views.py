from django.shortcuts import render
from ReservaCanchasUNA.models import Persona #importamos la base desde el principal

def inicio_ad(request):
    return render(request, 'administrador/inicio_admin.html')

def lista_usuarios(request):
    personas = Persona.objects.all()  # Traes todos los registros de Persona
    return render(request, 'administrador/lista_usuarios.html', {'personas': personas})