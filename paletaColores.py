class Paleta:
    """
    FILLME
    """
    def __init__(self,listaColores,resolucion):
        self.resolucion = resolucion
        self.setear(listaColores)

    def __str__(self):
        return str( "\n"  + "|-- " + "resolucion: " + str(self.resolucion))
        
    def limpiarGrilla(self):
        self.grilla = []
        for i in range(0,self.resolucion):
            self.grilla.append([0,0,0])
    
    def ajustarResolucion(self,listaColores,resolucion):
        # Esta funcion permite ajustar la paleta de colores cuando se cambia la resolucion.
        # mantiene la proporcion de la posicion respecto al total de la paleta.
        resoviejo = self.resolucion
        self.resolucion = resolucion

        for color in listaColores:
            color[2] = int(round((float(color[2])/resoviejo)*self.resolucion))
        
        self.setear(listaColores)
        return listaColores
    
    def setear(self,listaColores):
        # ListaColores es una lista de listas de 3 elementos cada una; donde cada lista de tres elementos consta de, color inicial, color final, longitud del tramo.
        # A su vez los colores son listas del tipo [R,G,B]
        # Ejemplos de llamadas a setear:
        #[[[colorinicial],[colorfinal],hasta],...]
        #p.setear([[[0,0,0],[100,100,100],99],[[200,0,200],[0,200,0],150],[[0,100,0],[100,0,100],255]])
        self.limpiarGrilla()

            # if(modo == "CS"): # listaColores: => [[R,G,B]]
                # # a toda la paleta le pone el mismo color
                # for i in range(0,self.resolucion):
                    # self.grilla[i][0] = listaColores[0][0] #R
                    # self.grilla[i][1] = listaColores[0][1] #G
                    # self.grilla[i][2] = listaColores[0][2] #B
            
            # if(modo == "MC"): # listaColores => [[R,G,B],[R,G,B]]
                # #interpolar entre el color listaColores[0] y listaColores[1] <<-- (Desde y hasta).
                # colorDesde = listaColores[0]
                # colorHasta = listaColores[1]
                # self.grilla = self.interpolarRGB(colorDesde,colorHasta,1,self.resolucion)[:]
                
            # if(modo == "NCS"): # listaColores => [[R,G,B,hasta],[R,G,B,hasta], ...]
                # desde = 0
                # for l in listaColores:
                    # hasta = l[3]
                    # for i in range(desde,hasta):
                        # self.grilla[i][0] = l[0]
                        # self.grilla[i][1] = l[1]
                        # self.grilla[i][2] = l[2]
                    # desde = hasta
                    
            # if(modo == "NMC"): #listaColores => [[[R,G,B],[R,G,B],hasta],[[R,G,B],[R,G,B],hasta], ...]
                # interpolar por partes, en lista colores se guarda una tupla, que tiene 3 items cada una; dos colores y hasta donde va ese tramo.
        desde = 0
        hasta = 0
        for l in listaColores:
            hasta = l[2]
            self.grilla[desde:hasta+1] = self.interpolarRGB(l[0],l[1],desde,hasta)[:]
            desde = hasta + 1
            
    def mostrar(self):
        for i in range(0,len(self.grilla)):
            print i+1, ":", self.grilla[i], ''
    
    def interpolarRGB(self,colorDesde,colorHasta,desde,hasta):
        #interpolacion lineal para colores, dados los puntos de inicio y fin y los colores en esos puntos, se calculan todos los intermedios(de manera lineal).
        grillaTemporal = []
        delta = hasta - desde - 1
        pasoRojo = float(colorHasta[0] - colorDesde[0])/delta
        pasoVerde= float(colorHasta[1] - colorDesde[1])/delta
        pasoAzul = float(colorHasta[2] - colorDesde[2])/delta

        #grillaTemporal.append(colorDesde)
        
        for i in range(0, delta+1): 
            rojo  = int(round(colorDesde[0] + (pasoRojo * i)))
            verde = int(round(colorDesde[1] + (pasoVerde * i))) 
            azul  = int(round(colorDesde[2] + (pasoAzul * i)))
            grillaTemporal.append([rojo,verde,azul])
    
        return grillaTemporal