from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey

# Create your models here.

class Persona(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    nombre = models.CharField(max_length=255)
    correo = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    id_calendario = models.CharField(max_length=255)

class Eventos(models.Model):
    id_persona = models.ForeignKey(Persona, on_delete=CASCADE)
    titulo = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    participantes = models.IntegerField()
    inicio = models.DateTimeField()
    termino = models.DateTimeField()

class Proyectos(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    nombre = models.CharField(max_length=255)
    
