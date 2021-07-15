from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import radioaficionados , estaciones_terrenas
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user

from .helpfunctions import concatpass

# Create your views here.
@unauthenticated_user
def loginUsr(request):
    if request.method == 'POST':
        usrname = request.POST['indicativoL']
        usrpass = request.POST['contrasenaL']
        usr_rad = authenticate(request, username = usrname, password = usrpass)

        if usr_rad is not None:
            login(request,usr_rad)
            #return HttpResponse('LogIn exitoso')
            return redirect("home")
        else: 
            messages.info(request,'Datos erroneos')
            #return HttpResponse('Datos erroneos')
        """if radioaficionados.objects.filter(indicativo = request.POST['indicativoL']).exists():
            tolog = radioaficionados.objects.get(indicativo = request.POST['indicativoL'])
            if tolog.password == request.POST['contrasenaL']:          
                return HttpResponse('LogIn exitoso')
            else:
                return HttpResponse('Datos erroneos')
        else :
            return HttpResponse('Indicativo equivocado')"""

    return render(request, "index.html")


def main(request):
    #return HttpResponse('Hello')
    rad = radioaficionados.objects.all()
    retUser = get_user_model()
    retusers = retUser.objects.all()
    print(rad)
    newlist = concatpass(rad,retusers)
    context = {
        'radio' : newlist,
        
    }
    return render(request,'radlist.html', context)

@unauthenticated_user
def register(request):
    if request.method == 'GET':
        return redirect('index')
    elif request.method == 'POST':
        #print(request.POST['indicativo'])
        
        new_rad = radioaficionados()
        new_rad.indicativo = request.POST['indicativoR']
        new_rad.password = request.POST['contrasenaR']
        new_rad.nombre = request.POST['nombreR']
        new_rad.apellidoP = request.POST['apellidoPR']
        new_rad.apellidoM = request.POST['apellidoMR']
        new_rad.municipio = request.POST['municipioR']
        new_rad.estado = request.POST['estadoR']
        new_rad.save()
        nuser = User.objects.create_user(new_rad.indicativo, '', new_rad.password)
        nuser.last_name = "{} {}".format(new_rad.nombre,new_rad.apellidoP)
        nuser.save()
        messages.success(request,'Usuario ' + new_rad.indicativo +' creado')
        return redirect('index')

@login_required(login_url='index')
def home(request):
    return render(request, "home.html")

@login_required(login_url='index')
def estacionTerrena(request):
    return render(request, "estacionTerrena.html")

@login_required(login_url='index')
def logoutUser(request):
    logout(request)
    return redirect("index")


"""def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    elif request.method == 'POST':
        #print(request.POST['indicativo'])
        new_rad = radioaficionados()
        new_rad.indicativo = request.POST['indicativo']
        new_rad.nombre = request.POST['nombre']
        new_rad.apellidoP = request.POST['apellidoP']
        new_rad.apellidoM = request.POST['apellidoM']
        new_rad.municipio = request.POST['municipio']
        new_rad.estado = request.POST['estado']
        new_rad.save()
        return redirect('index')"""


def estacionTerrena(request):
    usr = radioaficionados(request.user)
    tus_estaciones = estaciones_terrenas.objects.filter(indicativo=usr)
    context= {'estaciones' : tus_estaciones}
    if request.method == 'POST':
        new_est = estaciones_terrenas()
        new_est.nombre_estacion= request.POST['nombre']
        new_est.marca = request.POST['marca']
        new_est.modelo = request.POST['modelo']
        new_est.grid = request.POST['grid']
        new_est.antena = request.POST['antena']
        new_est.tipo_antena = request.POST['tipo']
        new_est.ganancia = request.POST['ganancia']
        new_est.polarizacion = request.POST['polarizacion']
        new_est.altura = request.POST['altura']
        new_est.modulacion = request.POST['formato']
        new_est.indicativo = usr # Lo del radioexperimentador
        #falta modulacion
        new_est.save() #Checar como es que se 

    return render(request,"estacionTerrena.html",context)#checar