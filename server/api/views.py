from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import radioaficionados , estaciones_terrenas ,bitacoras
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from itertools import islice
#import pandas as pd
import csv

from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users

from .helpfunctions import concatpass,ft_object
import time
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

@login_required(login_url='index')
@allowed_users(allowed_roles = ['administrators'])
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
def reportes(request):
    return render(request, "reportes.html")

@login_required(login_url='index')
def logoutUser(request):
    logout(request)
    return redirect("index")

def csvhandler(request):
    data = {}
    if "GET" == request.method:
        return render(request, "csvform.html")
    # if not GET, then proceed
    messages.info(request,"Subiendo ... ")
    try:
        radioa =radioaficionados.objects.get(indicativo='FFF')
        csv_file = request.FILES["csv_file"]
        fname = csv_file.name
        if (not fname.endswith('.csv')) and (not fname.endswith('.TXT')) and (not fname.endswith('.CSV')) and (not fname.endswith('.txt')) :

            messages.error(request,'File is not CSV or TXT type')
            return HttpResponse('Not a csv or txt')
        #if file is too large, return
        """if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponse('Archivo muy grande')
        """
        
        file_data = csv_file.read().decode("utf-8")		

        lines = file_data.split("\n")
        #loop over the lines and save them in db. If error , store as string and then display
        if csv_file.name.endswith('.csv') or csv_file.name.endswith('.CSV'):
            for line in lines:						
                fields = line.split(",")
                #""data_dict = {}
                """data_dict["name"] = fields[0]
                data_dict["start_date_time"] = fields[1]
                data_dict["end_date_time"] = fields[2]
                data_dict["notes"] = fields[3]"""
                print(fields)
        elif csv_file.name.endswith('.txt') or csv_file.name.endswith('.TXT'):
            cont = 0;
            print("entra")
            ftlist = []
            errlist = []
            for line in lines:
                line = line.rstrip()						
                fields = line.split(" ")
                fields = list(filter(None, fields))
                
                """objFT8 = {}
                objFT8["fecha"] = fields[0][0:6]
                objFT8["hora"] = fields[0][7:]
                objFT8["frecuencia"] = fields[1]
                objFT8["tx"] = fields[2] #Revisar
                objFT8["modo"] = fields[3]
                objFT8["ganancia"] = fields[4]
                objFT8["desfasamiento"] = fields[5]
                objFT8["canal"] = fields[6]
                objFT8["transmisor"] = fields[7]
                objFT8["receptor"] = fields[8]
                objFT8["mensaje"] = fields[9]"""
                cont+=1
                try:
                    
                    ftlist.append(bitacoras(
                        
                        indicativo=radioa,
                        fecha= "20{}-{}-{}".format(fields[0][0:2],fields[0][2:4],fields[0][4:6]),
                        hora= "{}:{}:{}".format(fields[0][7:9],fields[0][9:11],fields[0][11:]),
                        enlace= fields[1],
                        estacion_rec= fields[3],
                        grid= fields[5],
                        freq = fields[6],
                        modulacion = fields[7],
                        reporte1 =fields[8],
                        reporte2 = fields[9]
                    ))


                    """bitacoras.objects.update_or_create(
                        indicativo=radioa,
                        fecha= "20{}-{}-{}".format(fields[0][0:2],fields[0][2:4],fields[0][4:6]),
                        hora= "{}:{}:{}".format(fields[0][7:9],fields[0][9:11],fields[0][11:]),
                        enlace= fields[1],
                        estacion_rec= fields[3],
                        grid= fields[5],
                        freq = fields[6],
                        modulacion = fields[7],
                        reporte1 =fields[8],
                        reporte2 = fields[9]
                    )"""


                    """nuevab = bitacoras(indicativo=radioa,
                        fecha= "20{}-{}-{}".format(fields[0][0:2],fields[0][2:4],fields[0][4:6]),
                        hora= "{}:{}:{}".format(fields[0][7:9],fields[0][9:11],fields[0][11:]),
                        enlace= fields[1],
                        estacion_rec= fields[3],
                        grid= fields[5],
                        freq = fields[6],
                        modulacion = fields[7],
                        reporte1 =fields[8],
                        reporte2 = fields[9])
                    nuevab.save()"""

                    #
                except Exception as e:
                    messages.error(request,"Problema en fila ")
                    errlist.append(fields)
                #print(cont)
                #print(ft_object(fields))
                #time.sleep(.1)
                
                #print(objlist)
                #print(line)
            print(len(ftlist))
            print(len(errlist))
            #bitacoras.objects.bulk_create(ftlist, ignore_conflicts=True)
            batch_size = 100
            x=0
            while True:
                #batch = list(slice(ftlist,x,x+batch_size,batch_size))
                batch = list(islice(ftlist, x, x+batch_size))
                if not batch:
                    break
                bitacoras.objects.bulk_create(batch, batch_size, ignore_conflicts=True)
                x+=batch_size

            """while  x<len(ftlist):
                batch = ftlist[x:x+100]
                x+=100
                bitacoras.objects.bulk_create(batch, batch_size, ignore_conflicts=True)"""
            #print(errlist)

    except Exception as e:
    	#logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))
    
    return HttpResponse('Hecho')
        

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
    indestacion = None
    if request.method == 'GET':
        tus_estaciones = estaciones_terrenas.objects.filter(indicativo=usr)
        context= {'estaciones' : tus_estaciones, 'indestacion':indestacion}
    elif request.method == 'POST':
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
        new_est.indicativo = usr
        new_est.save()
        tus_estaciones = estaciones_terrenas.objects.filter(indicativo=usr)
        context= {'estaciones' : tus_estaciones, 'indestacion':indestacion}
    return render(request,"estacionTerrena.html",context)

def estacionTerrena2(request,indestacion):
    usr = radioaficionados(request.user)
    tus_estaciones = estaciones_terrenas.objects.filter(indicativo=usr)
    ind_est = estaciones_terrenas.objects.filter(indicativo=usr, nombre_estacion = indestacion)

    #context= {'estaciones' : tus_estaciones}
    if tus_estaciones and not ind_est == None:
        
        context= {'estaciones' : tus_estaciones, 'indestacion':ind_est}
    else:
        context= {'estaciones' : tus_estaciones, 'indestacion':None}
    
    if(indestacion == 'nueva'):
        return render(request,"estacionTerrena.html",context)
    else:
        return render(request,"estacionTerrena.html",context)


def pruebaestaciones(request,indestacion):
    #print(indestacion)
    usr = radioaficionados(request.user)
    tus_estaciones = estaciones_terrenas.objects.filter(indicativo=usr)
    ind_est = estaciones_terrenas.objects.filter(indicativo=usr, nombre_estacion = indestacion)
    
    if tus_estaciones and not ind_est == None :
        
        context= {'estaciones' : tus_estaciones, 'indestacion':ind_est}
    else:
        context= {'estaciones' : tus_estaciones, 'indestacion':None}

    return render(request,"pruebalista.html",context)#checar

def pruebaestaciones2(request):
    usr = radioaficionados(request.user)
    indestacion = None
    
    tus_estaciones = estaciones_terrenas.objects.filter(indicativo=usr)
    context= {'estaciones' : tus_estaciones, 'indestacion':indestacion}

    return render(request,"pruebalista.html",context)#checar

def reportes(request):
    usr = radioaficionados(request.user)
    tus_estaciones = estaciones_terrenas.objects.filter(indicativo=usr)
    context= {'estaciones' : tus_estaciones}
    return render(request, "reportes.html",context)