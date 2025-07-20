from django.shortcuts import render

# Create your views here.
def inicio_cor(request):
    return render(request, 'coordinador/inicio_cordinador.html')