from django.urls import path
from .views import main, register, loginUsr, home, estacionTerrena, logoutUser, csvhandler,estacionTerrena2

from .views import pruebaestaciones,pruebaestaciones2
urlpatterns = [
    
    path('', loginUsr, name="index"),
    #path('registro/', register, name="registrer"),
    path('register/', register, name="registrer"),
    path('radlist/', main, name="radlist"),
    path('home/', home, name="home"),
    path('estacionterrena/', estacionTerrena, name="estacionTerrena"),
    path('estacionterrena/<str:indestacion>', estacionTerrena2, name="estacionTerrena2"),
    path('logout/', logoutUser, name="logout"),
    path('csvprueba/', csvhandler, name="csvhandler"),
    path('pestacion/', pruebaestaciones2, name="pestacion"),
    path('pestacion/<str:indestacion>', pruebaestaciones, name="pestacionnum"),
    
]