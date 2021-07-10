from django.db import models

# Create your models here.
class radioaficionados(models.Model):
    indicativo = models.CharField(max_length=10,unique=True, primary_key=True)
    nombre = models.CharField(max_length=25, blank=False)
    apellidoP = models.CharField(max_length=25, blank=False)
    apellidoM = models.CharField(max_length=25, blank=False)
    municipio = models.CharField(max_length=30, blank=True)
    estado = models.CharField(max_length=30, blank=True)
    password = models.CharField(max_length=100, blank=False)

class bitacoras(models.Model):
    indicativo = models.ForeignKey(radioaficionados, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    enlace = models.CharField(max_length=10, blank=True)
    estacion_rec = models.CharField(max_length=10, blank=True)
    grid = models.CharField(max_length=5, blank=True)
    freq = models.FloatField()
    modulacion = models.CharField(max_length=10, blank=True)
    reporte1 = models.CharField(max_length=10, blank=True)
    reporte2 = models.CharField(max_length=10, blank=True)
