from django.db.models.fields import NullBooleanField
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import radioaficionados , estaciones_terrenas ,bitacoras, comentarios, mensajeadmin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from itertools import islice
#import pandas as pd
import csv

from .formvalidations import *

from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users

from .helpfunctions import concatpass,ft_object
import time

from django import template
from django.contrib.auth.models import Group

register = template.Library() 

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


# Create your views here.
@unauthenticated_user
def loginUsr(request):
    if request.method == 'POST':
        if(login_validation(request.POST)):
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
        if(register_validation(request.POST)):
            tempInd = request.POST['indicativoR']
            temppass = request.POST['contrasenaR']
            tempname = request.POST['nombreR']
            temppat = request.POST['apellidoPR']
            tempmat = request.POST['apellidoMR']
            tempmun = request.POST['municipioR']
            tempestado = request.POST['estadoR']
            flagVal = True

            if any(not c.isalnum() for c in tempInd) or (len(tempInd) < 4):
                messages.info(request,"Indicativo erroneo")
                flagVal = False
            
            if len(temppass) < 5:
                messages.info(request,"Contraseña invalida, se requiere una de mayor longitud")
                flagVal = False

            if any(not c.isalnum() for c in tempname):
                messages.info(request,"Nombre erroneo")
                flagVal = False
            if any(not c.isalnum() for c in temppat):
                messages.info(request,"Apellido Paterno erroneo")
                flagVal = False
            if any(not c.isalnum() for c in tempmat):
                messages.info(request,"Apellido Materno erroneo")
                flagVal = False
            
           

            if flagVal == True:
                
                try:
                    check = radioaficionados.objects.get(indicativo=request.POST['indicativoR']).indicativo
                except:
                    check = None
                
                if(check == None):
                    new_rad = radioaficionados()
                    new_rad.indicativo = request.POST['indicativoR']
                    new_rad.password = request.POST['contrasenaR']
                    new_rad.nombre = request.POST['nombreR']
                    new_rad.apellidoP = request.POST['apellidoPR']
                    new_rad.apellidoM = request.POST['apellidoMR']
                    new_rad.municipio = request.POST['municipioR']
                    new_rad.estado = request.POST['estadoR']
                    
                    nuser = User.objects.create_user(new_rad.indicativo, '', new_rad.password)
                    nuser.last_name = "{} {}".format(new_rad.nombre,new_rad.apellidoP)
                    nuser.save()
                    new_rad.password = 'No data'
                    new_rad.save()
                    messages.success(request,'Usuario ' + new_rad.indicativo +' creado')
                else:
                    messages.success(request,'Indicativo ' + request.POST['indicativoR'] +' ocupado.')

            return redirect('index')

@login_required(login_url='index')
def home(request):
    usr2 = request.user.groups.filter(name='analistas').exists()
    context={'grup': usr2}
    flagadmin = request.user.groups.filter(name='administrators').exists()
    context['adpriv']= flagadmin
    msgsadmin = mensajeadmin.objects.all()
    context['msgsadmin']= msgsadmin
    return render(request, "home.html", context)

@login_required(login_url='index')
def estacionTerrena(request):
    usr2 = request.user.groups.filter(name='analistas').exists()
    context={'grup': usr2}
    flagadmin = request.user.groups.filter(name='administrators').exists()
    context['adpriv']= flagadmin
    return render(request, "estacionTerrena.html",context)

@login_required(login_url='index')
def reportes(request):
    usr2 = request.user.groups.filter(name='analistas').exists()
    context={'grup': usr2}
    flagadmin = request.user.groups.filter(name='administrators').exists()
    context['adpriv']= flagadmin
    return render(request, "reportes.html",context)

@login_required(login_url='index')
def logoutUser(request):
    logout(request)
    return redirect("index")

@allowed_users(allowed_roles = ['analistas'])
@login_required(login_url='index')
def download(request):
    usr2 = request.user.groups.filter(name='analistas').exists()
    context={'grup': usr2}
    flagadmin = request.user.groups.filter(name='administrators').exists()
    context['adpriv']= flagadmin
    if request.method=="GET":
        return render(request,"downloads.html",context)
    elif request.method=="POST":
        if (date_validation(request.POST)):
            date1 = request.POST['date1']
            date2 = request.POST['date2']

            bitacorasQ = bitacoras.objects.filter(fecha__range=[date1,date2]).values_list('fecha', 'hora', 'mensaje1', 'mensaje2', 'modo', 'freq', 'mensaje3', 'indicativo_id', 'nombre_estacion', 'db', 'dt', 'freq_tx', 'rt')
           
            if not bitacorasQ:
                context = {'grup': usr2,'warning' : 'Al parecer no existen datos con estas fechas, intenta con otras fechas.'}
                return render(request,"downloads.html",context)
            else:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="bitacoras.csv"'
                writer = csv.writer(response)
                writer.writerow(['Fecha', 'Hora', 'Mensaje 1', 'Mensaje 2', 'Modo', 'Frecuencia', 'Mensaje 3', 'Indicativo Id', 'Nombre Estacion', 'DB', 'DT', 'Frecuencia TX', 'RT'])
                for bitacora in bitacorasQ:
                    writer.writerow(bitacora)
                return response
    
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
                #Falta tratar el archivo csv
                print(fields)
        elif csv_file.name.endswith('.txt') or csv_file.name.endswith('.TXT'):
            cont = 0
            print("entra")
            ftlist = []
            errlist = []
            for line in lines:
                line = line.rstrip()						
                fields = line.split(" ")
                fields = list(filter(None, fields))
                cont+=1
                try:
                    
                    ftlist.append(bitacoras(
                        
                        indicativo=radioa,
                        fecha= "20{}-{}-{}".format(fields[0][0:2],fields[0][2:4],fields[0][4:6]),
                        hora= "{}:{}:{}".format(fields[0][7:9],fields[0][9:11],fields[0][11:]),
                        enlace= fields[1],
                        rt = fields[2],
                        estacion_rec= fields[3],
                        grid= fields[5],
                        freq = fields[6],
                        modulacion = fields[7],
                        reporte1 =fields[8],
                        reporte2 = fields[9]
                    ))

                except Exception as e:
                    messages.error(request,"Problema en fila ")
                    errlist.append(fields)
                
            print(len(ftlist))
            print(len(errlist))
            batch_size = 100
            x=0
            while True:
                
                batch = list(islice(ftlist, x, x+batch_size))
                if not batch:
                    break
                bitacoras.objects.bulk_create(batch, batch_size, ignore_conflicts=True)
                x+=batch_size

    except Exception as e:
    	#logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))
    
    return HttpResponse('Hecho')
        
def estacionTerrena(request):
    usr = radioaficionados(request.user)
    tus_estaciones = estaciones_terrenas.objects.filter(indicativo=usr)
    usr2 = request.user.groups.filter(name='analistas').exists()
    context= {'estaciones' : tus_estaciones, 'grup': usr2}
    flagadmin = request.user.groups.filter(name='administrators').exists()
    
    print("Esto esta en flagadmin " , flagadmin)
    indestacion = None
    if request.method == 'GET':
        tus_estaciones = estaciones_terrenas.objects.filter(indicativo=usr)
        context= {'estaciones' : tus_estaciones, 'indestacion':indestacion, 'grup': usr2}
    elif request.method == 'POST':
        if(estaciones_validacion(request.POST)):
            new_est = estaciones_terrenas()
            new_est.nombre_estacion= request.POST['nombre']
            new_est.marca = request.POST['marca']
            new_est.modelo = request.POST['modelo']
            new_est.grid = request.POST['grid']
            new_est.antena = request.POST['antena']
            new_est.tipo_antena = request.POST['tipo']

            if(request.POST['ganancia'] == ""):
                new_est.ganancia = 0
            else:
                new_est.ganancia = request.POST['ganancia']

            new_est.polarizacion = request.POST['polarizacion']
            new_est.altura = request.POST['altura']

            if(request.POST['formato'] == "Otro"):
                new_est.modulacion = request.POST['formato-otro']
            else:
                new_est.modulacion = request.POST['formato']
            new_est.indicativo = usr
            new_est.save()
        tus_estaciones = estaciones_terrenas.objects.filter(indicativo=usr)
        context= {'estaciones' : tus_estaciones, 'indestacion':indestacion, 'grup': usr2}
        context['adpriv']= flagadmin
    return render(request,"estacionTerrena.html",context)

def estacionTerrena2(request,indestacion):
    usr = radioaficionados(request.user)
    usr2 = request.user.groups.filter(name='analistas').exists()
    flagadmin = request.user.groups.filter(name='administrators').exists()
    tus_estaciones = estaciones_terrenas.objects.filter(indicativo=usr)
    ind_est = estaciones_terrenas.objects.filter(indicativo=usr, nombre_estacion = indestacion)

    #context= {'estaciones' : tus_estaciones}
    if tus_estaciones and not ind_est == None:
        context= {'estaciones' : tus_estaciones, 'indestacion':ind_est, 'grup': usr2}
        
    else:
        context= {'estaciones' : tus_estaciones, 'indestacion':None, 'grup': usr2}
    context['adpriv']= flagadmin
    
    # if(indestacion == 'nueva'):
    #     return render(request,"estacionTerrena.html",context)
    # else:
    #     return render(request,"estacionTerrena.html",context)
    # return render(request, "estacionTerrena", context)
    return render(request,"estacionTerrena.html",context)

def estacionTerrenaDelete(request, idT):
    usr = radioaficionados(request.user)
    usr2 = request.user.groups.filter(name='analistas').exists()
    flagadmin = request.user.groups.filter(name='administrators').exists()
    
    tus_estaciones = estaciones_terrenas.objects.filter(indicativo=usr)
    indestacion = None
    context= {'estaciones' : tus_estaciones, 'indestacion':indestacion, 'grup': usr2}
    context['adpriv']= flagadmin
    # Que sea el dueño?
    estacion = estaciones_terrenas.objects.filter(id=idT)
    estacion.delete()
    
    return redirect('/estacionterrena/', context)

def estacionTerrenaUpdate(request, indestacion):
    usr = radioaficionados(request.user)

    if request.method == 'POST':
        if(request.POST['formato'] == "Otro"):
            modulacion = request.POST['formato-otro']
        else:
            modulacion = request.POST['formato']

        
        if not request.POST['ganancia']:
            gan = 0
        else:
            gan = int(request.POST['ganancia'])

        estaciones_terrenas.objects.filter(indicativo=usr, nombre_estacion = indestacion).update(
            nombre_estacion = request.POST['nombre'], 
            marca = request.POST['marca'],
            grid = request.POST['grid'],
            antena = request.POST['antena'],
            tipo_antena = request.POST['tipo'],
            ganancia = gan,
            polarizacion = request.POST['polarizacion'],
            altura = request.POST['altura'],
            modulacion = modulacion,
        )

    return HttpResponseRedirect("/estacionterrena/{indestacion}/".format(indestacion= request.POST['nombre']))

def pruebaestaciones(request,indestacion):
    #print(indestacion)
    usr = radioaficionados(request.user)
    usr2 = request.user.groups.filter(name='analistas').exists()
    flagadmin = request.user.groups.filter(name='administrators').exists()
    

    tus_estaciones = estaciones_terrenas.objects.filter(indicativo=usr)
    ind_est = estaciones_terrenas.objects.filter(indicativo=usr, nombre_estacion = indestacion)
    
    if tus_estaciones and not ind_est == None :
        
        context= {'estaciones' : tus_estaciones, 'indestacion':ind_est, 'grup': usr2}
    else:
        context= {'estaciones' : tus_estaciones, 'indestacion':None, 'grup': usr2}

    context['adpriv']= flagadmin
    return render(request,"pruebalista.html",context)#checar

def pruebaestaciones2(request):
    usr = radioaficionados(request.user)
    usr2 = request.user.groups.filter(name='analistas').exists()
    indestacion = None
    flagadmin = request.user.groups.filter(name='administrators').exists()
    
    tus_estaciones = estaciones_terrenas.objects.filter(indicativo=usr)
    context= {'estaciones' : tus_estaciones, 'indestacion':indestacion, 'grup': usr2}
    context['adpriv']= flagadmin
    return render(request,"pruebalista.html",context)#checar

def reportes(request):
    usr = radioaficionados(request.user)
    tus_estaciones = estaciones_terrenas.objects.filter(indicativo=usr)
    usr2 = request.user.groups.filter(name='analistas').exists()

    context= {'estaciones' : tus_estaciones, 'uploadFlag': False, 'grup': usr2}
    flagadmin = request.user.groups.filter(name='administrators').exists()
    
    print(" Variable usr ",usr)
    print(" Variable usr.indicativo ",usr.indicativo)
    data = {}
    if "GET" == request.method:
        #return render(request, "csvform.html")
        
        reports = bitacoras.objects.filter(indicativo=usr).order_by('id').reverse()[:100]
        context= {'estaciones' : tus_estaciones, 'uploadFlag': False, 'reports': reports, 'grup': usr2}   

        return render(request, "reportes.html",context)
    # if not GET, then proceed
    elif request.method == 'POST':
        messages.info(request,"Subiendo ... ")
        try:
            radioa =radioaficionados.objects.get(indicativo=usr.indicativo)
            csv_file = request.FILES["csv_file"]
            fname = csv_file.name
            if (not fname.endswith('.csv')) and (not fname.endswith('.TXT')) and (not fname.endswith('.CSV')) and (not fname.endswith('.txt')) :

                messages.error(request,'File is not CSV or TXT type')
                return render(request, "reportes.html",context)
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
                    #Falta tratar el archivo csv
                    print(fields)
            elif csv_file.name.endswith('.txt') or csv_file.name.endswith('.TXT'):
                cont = 0
                print("entra")
                ftlist = []
                errlist = []
                for line in lines:
                    line = line.rstrip()						
                    fields = line.split(" ")
                    fields = list(filter(None, fields))
                    cont+=1
                    try:
                        
                        ftlist.append(bitacoras(
                            
                            indicativo=radioa,
                            nombre_estacion = request.POST["estacion"],
                            fecha= "20{}-{}-{}".format(fields[0][0:2],fields[0][2:4],fields[0][4:6]),
                            hora= "{}:{}:{}".format(fields[0][7:9],fields[0][9:11],fields[0][11:]),
                            freq= fields[1],
                            rt = fields[2],
                            modo = fields[3],
                            db = fields[4],
                            dt = fields[5],
                            freq_tx = fields[6],
                            mensaje1 = fields[7],
                            mensaje2 =fields[8],
                            mensaje3 = fields[9],
                            
                        ))

                    except Exception as e:
                        #messages.error(request,"Problema en fila ")
                        errlist.append(fields)
                context["uploadFlag"] = True
                print(len(ftlist))
                print(len(errlist))
                batch_size = 100
                x=0
                while True:
                    
                    batch = list(islice(ftlist, x, x+batch_size))
                    if not batch:
                        break
                    bitacoras.objects.bulk_create(batch, batch_size, ignore_conflicts=True)
                    x+=batch_size

        except Exception as e:
            #logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
            messages.error(request,"Unable to upload file. "+repr(e))
        
        #return HttpResponse('Hecho')
        messages.info(request,"Completado")

        reports = bitacoras.objects.filter(indicativo=usr).order_by('id').reverse()[:100]
        context= {'estaciones' : tus_estaciones, 'uploadFlag': True, 'reports': reports, 'grup': usr2}     
        context['adpriv']= flagadmin
        return render(request, "reportes.html",context)

def handleComments(request):
    usr = radioaficionados(request.user)
    radioa =radioaficionados.objects.get(indicativo=usr.indicativo)
    tus_estaciones = estaciones_terrenas.objects.filter(indicativo=usr)
    usr2 = request.user.groups.filter(name='analistas').exists()

    reports = bitacoras.objects.filter(indicativo=usr).order_by('id').reverse()[:100]
    context= {'estaciones' : tus_estaciones, 'uploadFlag': False, 'reports': reports, 'grup': usr2}   
    flagadmin = request.user.groups.filter(name='administrators').exists()
    context['adpriv']= flagadmin
    print(request.POST['areacomment'])
    try:
        
        newcomment = comentarios(indicativo = radioa, comentario = request.POST['areacomment']) 
        newcomment.save()
        messages.info(request,"Gracias por tus comentarios. ")
    except Exception as e:
            #logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
            messages.error(request,"Error al guardar comentario, intentalo más tarde. "+repr(e))
    return render(request, "reportes.html",context)


@allowed_users(allowed_roles = ['administrators'])
@login_required(login_url='index')
def msgAdmin(request): 
    if request.method=="POST":
        newmsg = mensajeadmin()
        newmsg.cuerpoMsg = request.POST['msgbody']
        newmsg.save()
    msgs = mensajeadmin.objects.all()
    context = {"mensajesadmin": msgs}
    return render(request,"mensajesadmin.html",context)

@allowed_users(allowed_roles = ['administrators'])
@login_required(login_url='index')
def deletemsg(request,pk):
    mensajeadmin.objects.filter(id=pk).delete()
    return redirect('/mensajes/')
        

