from django.shortcuts import render

# Create your views here.
def inicio_es(request):
    return render(request, 'estudiante/inicio_estudiante.html')