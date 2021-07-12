
def concatpass(radlist, usrlist):
    newlist = []
    for rad in radlist:
        for usr in usrlist:
            #print(rad.indicativo)
            #print(usr.password)
            if(rad.indicativo == usr.username ):
                usrobj = {}
                usrobj['indicativo'] =  rad.indicativo
                usrobj['password'] =  rad.password
                usrobj['cpass'] =  usr.password
                usrobj['nombre'] =  rad.nombre
                usrobj['apellidoP'] =  rad.apellidoP
                usrobj['apellidoM'] =  rad.apellidoM
                usrobj['municipio'] =  rad.municipio
                usrobj['estado'] =  rad.estado
                newlist.append(usrobj)
    return newlist
                
