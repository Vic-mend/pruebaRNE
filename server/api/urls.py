from django.urls import path
from .views import main, register, loginUsr, home, estacionTerrena, reportes, logoutUser, csvhandler


urlpatterns = [
    
    path('', loginUsr, name="index"),
    #path('registro/', register, name="registrer"),
    path('register/', register, name="registrer"),
    path('radlist/', main, name="radlist"),
    path('home/', home, name="home"),
    path('estacionterrena/', estacionTerrena, name="estacionTerrena"),
    path('reportes/', reportes, name="reportes"),
    path('logout/', logoutUser, name="logout"),
    path('csvprueba/', csvhandler, name="csvhandler"),
]