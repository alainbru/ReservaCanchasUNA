from django.db import models

# Create your models here.
class Persona(models.Model):
    nombre = models.CharField(max_length=100, blank = True, null=True)
    apellidos = models.CharField(max_length=100, blank = True, null=True)