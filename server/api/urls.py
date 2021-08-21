from django.urls import path
from .views import *
from django.conf.urls import url

from .views import pruebaestaciones,pruebaestaciones2
urlpatterns = [
    
    path('', loginUsr, name="index"),
    #path('registro/', register, name="registrer"),
    path('register/', register, name="registrer"),
    path('radlist/', main, name="radlist"),
    path('home/', home, name="home"),
    path('estacionterrena/', estacionTerrena, name="estacionTerrena"),
    path('estacionterrena/<str:indestacion>/', estacionTerrena2, name="estacionTerrena2"),
    path('deleteEstacion/<int:idT>/', estacionTerrenaDelete, name="deleteEstacion"),
    path('updateEstacion/<str:indestacion>/', estacionTerrenaUpdate, name="updateEstacion"),
    path('logout/', logoutUser, name="logout"),
    path('csvprueba/', csvhandler, name="csvhandler"),
    path('pestacion/', pruebaestaciones2, name="pestacion"),
    path('pestacion/<str:indestacion>/', pruebaestaciones, name="pestacionnum"),
    path('reportes/', reportes, name="reportes"),
    path('commentary/', handleComments, name="handleComments"),
    path('download/', download, name="download"),
    path('download_usuarios/', download_usuarios, name="download_usuarios"),
    path('download_estaciones/', download_estaciones, name="download_estaciones"),
    path('download_reportes/', download_reportes, name="download_reportes"),
    path('mensajes/', msgAdmin, name="mensajesAdmin"),
    path('deletemsg/<str:pk>/', deletemsg, name="deletemsg"),
]