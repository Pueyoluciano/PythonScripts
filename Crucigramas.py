import time

palabras = ["pedro","ernesto","tres","atres","pos","zas","ywo"] # esta se carga segun las palabras a buscar, obvio. 
todasLasDirecciones = [(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]

grilla=[
["o","g","t","b","z","a","q","j","z"],
["y","r","s","q","r","b","q","r","h"],
["z","o","d","p","d","a","d","h","g"],
["n","t","a","e","e","e","i","o","i"],
["z","r","d","e","p","e","d","r","z"],
["a","b","c","e","e","e","f","g","h"],
["p","d","d","u","d","n","d","i","j"],
["t","r","l","l","r","u","p","r","k"],
["z","n","h","m","z","t","z","g","z"]
]

grilla=[
["p","e","d","r","o","j","u","k"],
["g","o","r","d","e","p","b","z"],
["i","g","q","n","z","p","o","a"],
["g","y","h","z","e","j","u","s"],
["q","w","e","r","t","s","b","q"],
["h","y","j","s","e","r","t","a"],
["g","t","b","f","q","y","w","o"]
]

# por cada palabra a buscar:
    # recorro la grilla letra por letra
        # if( para la palabraN encuentro su primer caracter en algun lugar de la grilla):
            # result = llamo a resolver palabra en caso base
            # if (result es distinto de 0): (si el resultado es 0 entonces la palabra no esta en esa posicion)
                # guardo la palabra con su poss inicial y direccion en Resultado
                 
    # Si recorri la grilla entera y no encontre la palabra, no existe en la grilla.
    
# resolver palabra:    
# if(no tengo direccion):
    # obtengo direcciones posibles(Esto es, tengo longitud suficiente para encontrar la palabra entera, sino ni me gasto).    
    # caso base (comienza la iteracion)
    
# else:
    # if (no llegue al final y letra siguiente es correcta):
        # caso iterativo
    # else: o llegue al final o letra incorrecta
        # if(llegue al final y letra correcta):
            # encontre palabra
        # else: 
            # no esta en esa direccion.
            
def generarGrilla():
    pass
        
def iterarPalabras():
    startTime = time.time()	
    for palabra in palabras:
        # print "busco palabra: " + palabras
        for x in range(0,len(grilla)):
            for y in range(0,len(grilla[0])):
                if(grilla[x][y] == palabra[0]):
                    # print "encontre una " + palabra[0] + " en " + str(x) + str(y)
                    result = resuelvePalabra(x,y, None, palabra, 0)
                    # print result    
    endTime = time.time()
    elapsedTime = endTime-startTime
    print "Resuelto en: " + str(elapsedTime)
    
def resuelvePalabra(x,y,direccion,palabra,numeroLetra):
    if(direccion == None):
        direcciones = obtenerDireccionesPosibles(palabra,x,y)
        for dir in direcciones:
            if(not(esUltimaLetra(palabra,numeroLetra)) and grilla[x+dir[0]][y+dir[1]] == palabra[numeroLetra + 1]):
                result = resuelvePalabra(x+dir[0], y+dir[1],dir,palabra,numeroLetra + 1)
                
            else:
                if(grilla[x+dir[0]][y+dir[1]] == palabra[numeroLetra + 1]):
                    print "encontre palabra " + palabra + " en direccion " + str(dir)
                    return "encontre palabra"
                # else:
                    # print "no encontre palabra end direccion" + str(dir)
    else:
        if(not(esUltimaLetra(palabra,numeroLetra)) and grilla[x+direccion[0]][y+direccion[1]] == palabra[numeroLetra + 1]):
            result = resuelvePalabra(x+direccion[0], y+direccion[1],direccion,palabra,numeroLetra + 1)
                
        else:
            if(esUltimaLetra(palabra,numeroLetra)):
                if(grilla[x][y] == palabra[numeroLetra]):
                    print "encontre palabra " + palabra + " en direccion " + str(direccion)
                    return "encontre palabra" 
                else:
                    # print "no encontre palabra en direccion" + str(direccion)
                    return 0
                
            else:
                # print "no encontre palabra en direccion" + str(direccion)
                return 0
               
def obtenerDireccionesPosibles(palabra,x,y):
    direccionesPosibles = []
    longitud = len(palabra) - 1
    maxX = len(grilla[0]) - 1
    maxY = len(grilla[1]) - 1
    
    #arriba
    
    if(y >= longitud):
        direccionesPosibles.append((0,-1))
        
    #arriba-derecha    
    if(y >= longitud and maxX - x >= longitud):
        direccionesPosibles.append((1,-1))
        
    #derecha
    if(maxX - x >= longitud):
        direccionesPosibles.append((1,0))
        
    #abajo-derecha    
    if(maxY - y >= longitud and maxX - x >= longitud):
        direccionesPosibles.append((1,1))
        
    #abajo    
    if(maxY - y >= longitud):
        direccionesPosibles.append((0,1))
        
    #abajo-izquierda
    if(maxY - y >= longitud and x >= longitud):
        direccionesPosibles.append((-1,1))
        
    #izquierda
    if(x >= longitud):
        direccionesPosibles.append((-1,0))
        
    #arriba-izquierda
    if(maxY - y >= longitud and x >= longitud):
        direccionesPosibles.append((-1,-1))

    # print direccionesPosibles
    return direccionesPosibles
                
def esUltimaLetra(palabra,numeroLetra):
    if(len(palabra) - 1 - numeroLetra == 0): 
        return True
    else:
        return False

def mostrarGrilla():
    for fila in grilla:
        for columna in fila:
            print columna,
        print "\n"
        
print palabras
mostrarGrilla()     
iterarPalabras()