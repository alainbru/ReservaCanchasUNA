from django.shortcuts import render

def inicio_ad(request):
    return render(request, 'administrador/inicio_admin.html')