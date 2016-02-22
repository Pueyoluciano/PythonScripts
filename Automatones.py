import os
import Aplicacion
import math
import random
from datetime import datetime
from Menu import *
from Variable import *
#------------------------------------------------
#--------------- TODO ---------------------------
#------------------------------------------------
# 1) SESION DE AUTOMATAS
# 2) INTERFAZ GRAFICA

#------------------------------------------------
#------------------------------------------------
#------------------------------------------------
class Automatones(Aplicacion.Aplicacion):
    
    """
    FILLME
    """

    def iniciar(self,**args):
    
        self.mapaReglas = {}
        self.grilla =[[]]
        self.grillaOpciones = {"medio":self.iniciarGrillaMedio,
                                "vacia":self.iniciarGrillaVacia,
                                "llena":self.iniciarGrillaLlena,
                                "random":self.iniciarGrillaRandom,
                                "principio":self.iniciarGrillaPrincipio,
                                "final":self.inciarGrillaFinal}
        
        self.vars["charset"] = Variable([".","#"],self.modifCharSet) 
        self.vars["tamano"] = Variable(11,self.modifTamano,minimo=2) 
        self.vars["iteraciones"] = Variable(10,self.modifGenerico,minimo=1) 
        self.vars["regla"] = Variable(110,self.modifRegla,minimo=0,maximo=255) # 01101110 bin = 110 dec
        self.vars["grillaInicial"] = Variable("medio",self.modifFuncionGeneradora)
        self.vars["outFile"] = Variable(self.appNombre + "Out.txt",self.modifPath,orden=204)
        
        leaf1 = Leaf("Generar","Escribe el archivo de salida con el automata configurado",self.generar)
        leaf2 = Leaf("pasar a decimal","pasar un numero binario a decimal",self.pasarADecimal)
        leaf3 = Leaf("pasar a binario","pasar un numero decimal a binario",self.pasarABinario)
        self.agregarMenu(0,leaf1)
        self.agregarMenu(-2,leaf2)
        self.agregarMenu(-2,leaf3)
        
        self.agregarPostFunciones(self.generar)
        
        self.iniciarMapa(self.vars["regla"].valor)
        self.iniciarGrilla()

    def iniciarGrilla(self):
        self.grilla = [[]]  
        clave = self.vars["grillaInicial"].valor
        self.grillaOpciones[clave]()
    
    def inciarGrillaFinal(self):
        self.grilla = [[]]
        for i in range(0,self.vars["tamano"].valor):
            if(i == self.vars["tamano"].valor - 1):
                self.grilla[0].append("1")
            else:
                self.grilla[0].append("0")
        
    def iniciarGrillaPrincipio(self):
        self.grilla = [[]]
        for i in range(0,self.vars["tamano"].valor):
            if(i == 0):
                self.grilla[0].append("1")
            else:
                self.grilla[0].append("0")
        
    def iniciarGrillaMedio(self):
        self.grilla = [[]]
        mitad =self.vars["tamano"].valor/2
        espar = not(self.vars["tamano"].valor%2)
        for i in range(0,self.vars["tamano"].valor):
            if(i == mitad or (espar and i == mitad-1)):
                self.grilla[0].append("1")
            else:
                self.grilla[0].append("0")
    
    def iniciarGrillaVacia(self):
        self.grilla = [[]]
        for i in range(0,self.vars["tamano"].valor):
            self.grilla[0].append("0")
    
    def iniciarGrillaLlena(self):
        self.grilla = [[]]
        for i in range(0,self.vars["tamano"].valor):
            self.grilla[0].append("1")

    def iniciarGrillaRandom(self):
        self.grilla = [[]]
        for i in range(0,self.vars["tamano"].valor):
            self.grilla[0].append(random.choice(["0","1"]))
            
    def iniciarMapa(self,regla):
        regla = self.toBin(regla,8)
        self.mapaReglas = {"000":regla[7],
                            "001":regla[6],
                            "010":regla[5],
                            "011":regla[4],
                            "100":regla[3],
                            "101":regla[2],
                            "110":regla[1],
                            "111":regla[0]}
        
    def modifCharSet(self,key):
        self.vars["charset"].valor[0] = validador.ingresar(str)
        self.vars["charset"].valor[1] = validador.ingresar(str)

    def modifRegla(self,key):
        regla = validador.ingresar(int,validador.entre,self.vars["regla"].minimo,self.vars["regla"].maximo)
        
        self.vars["regla"].valor = regla
        
        regla = self.toBin(regla,8)
        self.mapaReglas["111"] = regla[0]
        self.mapaReglas["110"] = regla[1]
        self.mapaReglas["101"] = regla[2]
        self.mapaReglas["100"] = regla[3]
        self.mapaReglas["011"] = regla[4]
        self.mapaReglas["010"] = regla[5]
        self.mapaReglas["001"] = regla[6]
        self.mapaReglas["000"] = regla[7]   
            
    def modifGrilla(self,key):
        exponente = 2**self.vars["iteraciones"].valor
    
        grilla = validador.ingresar(int,validador.entre,0,exponente)
        print self.toBin(grilla,exponente)

        #self.grilla[0] = self.toBin(grilla,exponente)
    
    def modifFuncionGeneradora(self,key):
        for (i,clave) in enumerate(self.grillaOpciones.keys()):
            print str(i+1) + ") " + clave
        
        key = validador.seleccionar(self.grillaOpciones.keys())
        self.vars["grillaInicial"].valor = key
        self.iniciarGrilla()

    def modifTamano(self,key):
        self.vars["tamano"].valor = validador.ingresar(int,validador.entre,self.vars["tamano"].minimo, self.vars["tamano"].maximo)
        self.iniciarGrilla()
        
    def generar(self):      
        grillaAux = self.grilla[:]
        print grillaAux
        for i in range(0,self.vars["iteraciones"].valor):
            grillaAux.append([])
            for j in range(0,self.vars["tamano"].valor):
                # en estos IF se arma el numero binario de 3 digitos, que forman la vecindad. la vecindad es el punto que estoy mirando y los puntos inmediatos a su derecha e izquierda. cada punto tiene un 1 o un 0, en total formando un numero de 3 digitos binario, este numero es el indice de mi mapa de reglas, y asi se decide como se pintara el punto del medio en la siguiente iteracion.
                if(j == 0):
                    vecindad = "0" + grillaAux[i][j] + grillaAux[i][j+1]
                    
                else: 
                    if(j == self.vars["tamano"].valor - 1):
                        vecindad = grillaAux[i][j-1] + grillaAux[i][j] + "0"
                    
                    else:
                        vecindad = grillaAux[i][j-1] + grillaAux[i][j] + grillaAux[i][j+1]

                grillaAux[i+1].append(self.aplicarRegla(vecindad))
                
        self.escribirOUT(grillaAux)
        return grillaAux[0] #retorno la ultima linea de la grilla
        
    def aplicarRegla(self,vecindad):
        return self.mapaReglas[vecindad]

    def escribirOUT(self,grilla):
        archivo = open(self.vars["outFile"].valor,"w")
        archivo.write(str(self.vars) + "\n")
        archivo.write("Creado: " + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "\n")

        for i in range(0,self.vars["iteraciones"].valor):
            for j in range(0,self.vars["tamano"].valor):
                indice = int(grilla[i][j])
                char = self.vars["charset"].valor[indice]
                archivo.write(char)
            archivo.write("\n")
        archivo.close()
    
    def pasarABinario(self):
        print bin(validador.ingresar(int))[2:]
        
    def pasarADecimal(self):
        try:
            print int("0b" + str(int(validador.ingresar(str))),2)
        except(ValueError):
            print "mandaste Fruta wacho, solo 1 y 0"        
    
    def toBin(self,decimal,longitud):
        return bin(decimal)[2:].zfill(longitud)
    
    def ayuda(self):
        self.espaciador()
        print "--- Manual de referencia" + self.appNombre + self.version + " ----------------------"
        print "----------------------------------------------------------------"
        print "1)Que Cuerno es un automata celular?\n"
        print "Las definiciones rigurosas sobre automatas celulares son        "
        print "dificiles de entender y no tienen mucha utilidad para lo que    "
        print "hacemos aca."
        print "lo que hace falta entender es que el automata celular que imple-"
        print "mentamos lee una grilla de puntos con 1s y 0s y en base a una   "
        print "regla en particular decide si esos 1s y 0s se modifican o no,   "
        print "luego escribe una fila debajo de la primera en base a estas de- "
        print "cisiones."
        print "algunas reglas(mas abajo se habla en detalle sobre las reglas)  "
        print "tienen la propiedad de ser Turing Completas (otro bardo mas :D) "
        print "pero un corolario de esto es que tienen la misma capacidad de   "
        print "computo que una computadora convencional (eso no quiere decir   "
        print "que sean igual de rapidos ni igual de facil de programar).      "
        print ""
        print "2) Reglas y vecindades\n"
        print "Entrando mas en detalle, cada punto de la grilla; el cual posee "
        print "un 1 o un 0, tiene una vecindad asociada. Esta es:              "
        print "el punto a su izquierda, el mismo y el punto a su derecha.      "
        print "esto forma un grupo de 3 numeros de la pinta xxx donde las x son" 
        print "1 o 0."
        print "esto nos da 8 combinaciones posibles:\n"
        print "000\n001\n010\n011\n100\n101\n110\n111\n"
        print "para cada una de estas vecindades, la regla nos dice que sudece "
        print "en la proxima iteracion con el punto asociado a dica vecindad.\n"
        print "vecindad: 000 001 010 011 100 101 110 111"
        print "regla:     x1  x2  x3  x4  x5  x6  x7  x8\n"
        print "cada xn puede ser un 1 o un 0, eso nos da 2**8 combinaciones    "
        print "posibles, y de ahi que las relgas obtienen su nombre, pasando a "
        print "decimal esos valores, por ej:"
        print "00001101 = 26   <- este dibuja un triaguno de sierpinski"
        print "01101110 = 110 <- este es Turing Completo :D"
        self.espaciador()
        
        
if __name__ == '__main__':  
    a = Automatones("Automatones","1.0.0",False)
    a.menuPrincipal()       