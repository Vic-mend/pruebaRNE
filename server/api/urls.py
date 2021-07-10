

from django.urls import path
from .views import main,register, login


urlpatterns = [
    
    path('', login, name="index"),
    #path('registro/', register, name="registrer"),
    path('register/', register, name="registrer"),
    path('radlist/', main, name="registrer"),
]