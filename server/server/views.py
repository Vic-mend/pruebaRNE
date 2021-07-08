from django.http import HttpResponse
import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    #html = "<html><body>It is now %s.</body></html>" % now
    html= """
    <html> 
        <body>
            <h1>It is now %s.</h1>
        </body>
    </html>
    """% now
    return HttpResponse(html)

def saludo(request): #primera vista

    return HttpResponse("Hola alumnos esta es nuestra primera página con django")

def despedida(request): #segunda

    return HttpResponse("Adios")

def calculaEdad(request, agno, edadActual): #request, _ -> parametros que quieras

    #edadActual=21
    periodo=agno-2021
    edadFutura=edadActual+periodo
    html="<html><body><h2> En el año %s tendrás %s años</body></html>" %(agno,edadFutura)

    return HttpResponse(html)
