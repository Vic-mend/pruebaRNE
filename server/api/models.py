from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.
class radioaficionados(models.Model):
    
    indicativo = models.CharField(max_length=10,unique=True, primary_key=True)
    nombre = models.CharField(max_length=25, blank=False)
    apellidoP = models.CharField(max_length=25, blank=False)
    apellidoM = models.CharField(max_length=25, blank=False)
    municipio = models.CharField(max_length=30, blank=True)
    estado = models.CharField(max_length=30, blank=True)
    password = models.CharField(max_length=100, blank=False)
    #USERNAME_FIELD = 'indicativo'
    #REQUIRED_FIELDS = [indicativo,password]

class bitacoras(models.Model):
    indicativo = models.ForeignKey(radioaficionados, on_delete=models.CASCADE)
    nombre_estacion = models.CharField(max_length=30, blank=False, default='Sin Estacion')
    fecha = models.DateField()
    hora = models.TimeField()
    enlace = models.CharField(max_length=10, blank=True)
    estacion_rec = models.CharField(max_length=10, blank=True)
    grid = models.CharField(max_length=5, blank=True)
    freq = models.FloatField()
    modulacion = models.CharField(max_length=10, blank=True)
    reporte1 = models.CharField(max_length=10, blank=True)
    reporte2 = models.CharField(max_length=10, blank=True)

class estaciones_terrenas(models.Model):
    indicativo = models.ForeignKey(radioaficionados, on_delete=models.CASCADE)
    nombre_estacion = models.CharField(max_length=30, blank=False)
    marca = models.CharField(max_length=30, blank=False)
    modelo = models.CharField(max_length=40, blank=False)
    antena = models.CharField(max_length=30, blank=False)
    tipo_antena = models.CharField(max_length=20 ,blank=False)
    ganancia = models.IntegerField(blank=True)
    frecuencia = models.CharField(max_length=20, blank=False)
    polarizacion  = models.CharField(max_length=20, blank=False)
    altura = models.DecimalField(max_digits=7, decimal_places=4, blank=False)
    modulacion = models.CharField(max_length=10, blank=False, null=True)
    grid = models.CharField(max_length=10, blank=False)

class comentarios(models.Model):
    indicativo = models.ForeignKey(radioaficionados, on_delete=models.CASCADE)
    comentario = models.CharField(max_length=600, blank=False)