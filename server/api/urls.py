from django.urls import path
from .views import main, register, loginUsr, home, estacionTerrena, logoutUser


urlpatterns = [
    
    path('', loginUsr, name="index"),
    #path('registro/', register, name="registrer"),
    path('register/', register, name="registrer"),
    path('radlist/', main, name="radlist"),
    path('home/', home, name="home"),
    path('estacionterrena/', estacionTerrena, name="estacionTerrena"),
    path('logout/', logoutUser, name="logout"),
    path('csvprueba/', csvhandler, name="csvhandler"),
]