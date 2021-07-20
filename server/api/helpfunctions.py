
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
                
def ft_object(fields):
    objftocho = {}
    objftocho["fecha"] = fields[0][0:6]
    objftocho["hora"] = fields[0][7:]
    objftocho["frecuencia"] = fields[1]
    objftocho["tx"] = fields[2] #Revisar
    objftocho["modo"] = fields[3]
    objftocho["ganancia"] = fields[4]
    objftocho["desfasamiento"] = fields[5]
    objftocho["canal"] = fields[6]
    objftocho["transmisor"] = fields[7]
    objftocho["receptor"] = fields[8]
    objftocho["mensaje"] = fields[9]
    return objftocho
