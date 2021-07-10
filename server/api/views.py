from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import radioaficionados 
# Create your views here.
def login(request):
    return render(request, "index.html")


def main(request):
    #return HttpResponse('Hello')
    rad = radioaficionados.objects.all()
    print(rad)
    context = {
        'radio' : rad
    }
    return render(request,'radlist.html', context)

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
        
        return redirect('index')

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




