from django.urls import path
from .views import main,register,loginUsr,home,logoutUser,estaciones


urlpatterns = [
    
    path('', loginUsr, name="index"),
    #path('registro/', register, name="registrer"),
    path('register/', register, name="registrer"),
    path('radlist/', main, name="radlist"),
    path('home/', home, name="home"),
    path('logout/', logoutUser, name="logout"),
    path('station/', estaciones , name = "estaciones")
]