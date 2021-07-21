
def estaciones_validacion(values):
  val = True 
  if(len(values['nombre']) > 30 or len(values['nombre']) < 1 ): val=False
  if(len(values['marca']) > 30 or len(values['marca']) < 1 ): val=False
  if(len(values['modelo']) > 40 or len(values['modelo']) < 1 ): val=False
  if(len(values['grid']) > 20 or len(values['grid']) < 1 ): val=False
  if(len(values['antena']) > 30 or len(values['antena']) < 1 ): val=False
  if(len(values['tipo']) > 30 or len(values['tipo']) < 1 ): val=False
  if(len(str(values['ganancia'])) < 0 ): val=False
  if(len(values['polarizacion']) > 20 or len(values['polarizacion']) < 1 ): val=False
  if(len(str(values['altura'])) > 7 or len(str(values['altura'])) < 1 ): val=False
  if(len(values['formato']) > 10 or len(values['formato']) < 1 ): val=False
  if(values['formato'] == "Otro"):
    if(len(values['formato-otro']) > 10 or len(values['formato-otro']) < 1 ): val=False

  return val