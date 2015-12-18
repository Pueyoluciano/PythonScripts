import Aplicacion
import random
import os
import time
from Menu import *
from Variable import *
from validador import *
#------------------------------------------------
#--------------- TODO ---------------------------
#------------------------------------------------

#------------------------------------------------
#------------------------------------------------
#------------------------------------------------
class Crucigrammer(Aplicacion.Aplicacion):
    def iniciar(self,**args):	
	#-----------------------
	#--- inicializacion ----
	#-----------------------
		#variables de programa
        self.grilla = []
        self.grillaSoloResultado = []
        self.possTemporal = []
        self.grillaCrucigrama = "grillaCrucigrama.txt"
        # self.palabras = ["pedro","ernesto","tres","atres","pos","zas","ywo"] # esta se carga segun las palabras a buscar, obvio.
        self.palabras = ["dia", "via", "oro", "roto", "ocho", "mono", "cuatro", "cinco", "perro", "luchas", "piedra", "sismos", "luciano", "quiebro", "sorongo", "filantropo", "destructor"] # esta se carga segun las palabras a buscar, obvio.
        self.resultado = [] #[palabra:"Pedro",x:5,y:6,direccion:(1,1)]
        self.abcdario = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        
		#variables de usuario	
        self.vars["relleno"] = Variable("-",self.modifGenerico,orden=0)
        self.vars["ancho"] = Variable(10,self.modifGenerico,minimo=3,orden=1)
        self.vars["alto"] = Variable(10,self.modifGenerico,minimo=3,orden=2)
		
		#Items del Menu
        self.agregarMenu(0,Leaf("Resolver","Realizando busqueda de palabras...",self.iterarPalabras))
        self.agregarMenu(1,Leaf("Generar Crucigrama","",self.generarCrucigrama))
        self.agregarMenu(2,Leaf("Rellenar Crucigrama","",self.rellenarConRandom))
        self.agregarMenu(3,Leaf("Recargar Crucigrama","", self.cargarCrucigrama))
        self.agregarMenu(4,Leaf("Modificar Crucigrama","",self.modificarCrucigrama))
        self.agregarMenu(5,Nodo("Palabras a buscar","",Leaf("Agregar Palabras","",self.agregarPalabras), Leaf("Quitar Palabras","",self.quitarPalabras)))
        
        #Funciones que se ejecutan luego de llamar a Modificar.
        # self.agregarPostFunciones()
		
        self.cargarCrucigrama()
        
	#-----------------------
	#--- Funciones ---------
	#-----------------------
    def agregarPalabras(self):
        print "Palabras actuales:"
        print self.palabras
        print "escriba las palabras a agregar separadas por espacios:"
        nuevasPalabras = validador.ingresar(str)
        
        for palabra in nuevasPalabras.split():
            if(not palabra in self.palabras):
                self.palabras.append(palabra)
                print "se agrego: " + palabra
                
        self.pausa()
            
    def quitarPalabras(self):
        print "Palabras actuales:"
        self.enumerarLista(self.palabras)
        print "ingrese el numero de orden de las palabras a qutiar separados por espacios:"
        palabrasQuitar = validador.ingresar(str) 
        
        aRemover = []
        for palabra in palabrasQuitar.split():
            try:
                aRemover.append(self.palabras[int(palabra) - 1])
                temporal = self.palabras[int(palabra) - 1]
                print "se quito: " + temporal
                
            except:
                print palabra + ": valor invalido"
            
        self.palabras = [palabra for palabra in self.palabras if palabra not in aRemover]
            
        self.pausa()
    
    def generarCrucigrama(self):
        self.grilla = self.grillaVacia(self.vars["ancho"].valor,self.vars["alto"].valor)

        startTime = time.time()
        
        palabrasNuevas = self.palabras
        random.shuffle(palabrasNuevas)
        
        for palabra in palabrasNuevas:
            lugares = self.obtenerLugaresPosibles(palabra)
            if (lugares == []):
                self.espaciador()
                print "La palabra " + palabra + " no puede ser ubicada"
                print "Esto puede ser porque: "
                print "1) Sus dimensiones son mayores que la grilla actual"
                print "2) En el reparto de palabras se quedo sin lugares posibles"
                print "Siempre revisar que la longitud de las palabras sea menor o igual que el ancho y alto de la grilla"
                self.pausa()
            else:
                lugarFinal = random.choice(lugares)
                x = lugarFinal[0]
                y = lugarFinal[1]
                direccion = random.choice(lugarFinal[2])
                print palabra, x , y ,direccion, self.traducirDireccion(direccion)
                self.escribirPalabra(palabra,x,y,direccion)
        
        self.escribirCrucigrama()
        
        endTime = time.time()
        elapsedTime = endTime-startTime
        print "Tiempo de generacion: " + str(elapsedTime)
        
    def rellenarConRandom(self):
        for x in range(0, len(self.grilla)):
            for y in range(0, len(self.grilla[0])):
                if(self.grilla[x][y] == self.vars["relleno"].valor):
                    self.grilla[x][y] = random.choice(self.abcdario)
        
        self.escribirCrucigrama()
        
    def obtenerLugaresPosibles(self,palabra):
        lugaresPosibles = []
        for x in range(0,len(self.grilla)):
            for y in range(0,len(self.grilla[0])):

                direcciones = self.obtenerDireccionesPosibles(palabra,x,y)
                
                if([direccion for direccion in direcciones if self.macheaPalabraEnGrilla(palabra,x,y,direccion)] != []):
                    lugaresPosibles.append([x,y,[direccion for direccion in direcciones if self.macheaPalabraEnGrilla(palabra,x,y,direccion)]])
                    
        return lugaresPosibles        
   
    def macheaPalabraEnGrilla(self,palabra,x,y,dir):
        i = 0
        
        for letra in palabra:
        
            letraGrilla = self.grilla[x + (dir[0]*i)][y + (dir[1]*i)]
            if(letraGrilla != letra and letraGrilla != self.vars["relleno"].valor):
                return 0
            i+=1
            
        return 1

    def escribirCrucigrama(self):
        archivo = open(self.vars["filesPath"].valor + "\\" +self.grillaCrucigrama,"w")
        
        for x in range(0, len(self.grilla)):
            for y in range(0, len(self.grilla[0])):
                archivo.write(self.grilla[x][y])
            archivo.write("\n")
            
        archivo.close()
    
    def escribirPalabra(self,palabra,x,y,dir):
        i = 0
        for letra in palabra:
            self.grilla[x + (dir[0]*i)][y + (dir[1]*i)] = letra
            i+=1
            
    def iterarPalabras(self):
        self.resultado = []
        startTime = time.time()	
        for palabra in self.palabras:
            # print "busco palabra: " + palabras
            for x in range(0,len(self.grilla)):
                for y in range(0,len(self.grilla[0])):
                    if(self.grilla[x][y] == palabra[0]):
                        # me guardo el punto donde empiezo a buscar, si encontre palabra, lo guardo como resultado
                        self.possTemporal = [x,y]
                        result = self.resuelvePalabra(x,y, None, palabra, 0)
                        
        endTime = time.time()
        elapsedTime = endTime-startTime
        
        self.espaciador()
        self.cargarGrillaResultado()
        self.mostrarGrilla(self.grillaSoloResultado)
        self.mostrarResultado()
        self.espaciador()
        self.pausa()
        
        print "Resuelto en: " + str(elapsedTime)
    
    def resuelvePalabra(self,x,y,direccion,palabra,numeroLetra):
        if(direccion == None):
            direcciones = self.obtenerDireccionesPosibles(palabra,x,y)
            for dir in direcciones:
                if(not(self.esUltimaLetra(palabra,numeroLetra)) and self.grilla[x+dir[0]][y+dir[1]] == palabra[numeroLetra + 1]):
                    result = self.resuelvePalabra(x+dir[0], y+dir[1],dir,palabra,numeroLetra + 1)
                    
                else:
                    if(self.grilla[x+dir[0]][y+dir[1]] == palabra[numeroLetra + 1]):
                        # print "encontre palabra " + palabra + " en direccion " + str(dir)
                        self.resultado.append([palabra,self.possTemporal[0],self.possTemporal[1],dir])
                        return "encontre palabra"
                    # else:
                        # print "no encontre palabra end direccion" + str(dir)
        else:
            if(not(self.esUltimaLetra(palabra,numeroLetra)) and self.grilla[x+direccion[0]][y+direccion[1]] == palabra[numeroLetra + 1]):
                result = self.resuelvePalabra(x+direccion[0], y+direccion[1],direccion,palabra,numeroLetra + 1)
                    
            else:
                if(self.esUltimaLetra(palabra,numeroLetra)):
                    if(self.grilla[x][y] == palabra[numeroLetra]):
                        # print "encontre palabra " + palabra + " en direccion " + str(direccion)
                        self.resultado.append([palabra,self.possTemporal[0],self.possTemporal[1],direccion])
                        return "encontre palabra" 
                    else:
                        # print "no encontre palabra en direccion" + str(direccion)
                        return 0
                    
                else:
                    # print "no encontre palabra en direccion" + str(direccion)
                    return 0
    
    def mostrarResultado(self):
        for encuentro in self.resultado:
            print "- " + encuentro[0] + " - ",
            print "X: " + str(encuentro[2]) + " Y: "+ str(encuentro[1]),
            print "- Direccion: " + str(self.traducirDireccion(encuentro[3]))
    
    def grillaVacia(self,ancho,alto):
        return [[self.vars["relleno"].valor for i in range(0,ancho)] for j in range(0,alto)]
        
    def cargarGrillaResultado(self):
        self.grillaSoloResultado = self.grillaVacia(len(self.grilla[0]),len(self.grilla))
        for palabra in self.resultado:
            #[palabra:"Pedro",x:5,y:6,direccion:(1,1)]
            i = 0
            for letra in palabra[0]:
                # palabra[1] = x
                # palabra[2] = y
                # palabra[3][0] = direccionX
                # palabra[3][1] = direccionY
                
                self.grillaSoloResultado[palabra[1] + (palabra[3][0] * i)][palabra[2] + (palabra[3][1] * i)] = letra
                i += 1
    
    def traducirDireccion(self,dir):           
        if(dir == (-1,0)):
            return "arriba"
            
        if(dir == (-1,1)):
            return "derecha-arriba"
            
        if(dir == (0,1)):
            return "derecha"
            
        if(dir == (1,1)):
            return "derecha-abajo"
            
        if(dir == (1,0)):
            return "abajo"
            
        if(dir == (1,-1)):
            return "izquierda-abajo"
            
        if(dir == (0,-1)):
            return "izquierda"
            
        if(dir == (-1,-1)):
            return "izquierda-arriba"
                        
        return "ups"    
        
    def obtenerDireccionesPosibles(self,palabra,x,y):
        direccionesPosibles = []
        longitud = len(palabra) - 1
        maxX = len(self.grilla) - 1
        maxY = len(self.grilla[0]) - 1
        
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
        if(y >= longitud and x >= longitud):
            direccionesPosibles.append((-1,-1))

        # print direccionesPosibles
        return direccionesPosibles
                
    def esUltimaLetra(self,palabra,numeroLetra):
        if(len(palabra) - 1 - numeroLetra == 0): 
            return True
        else:
            return False

    def mostrarGrilla(self,grilla):
        if(grilla == []):
            print "- grilla vacia -"
            
        else:
            print "-",
            for h in range(0,len(grilla[0])):
                print str(h),
            print ""
            for i in range(0,len(grilla)):
                print str(i),
                for j in range(0,len(grilla[i])):
                    print grilla[i][j],
                print "\n"

    def crearGrilla(self):
        if not(os.path.exists(self.vars["filesPath"].valor + "\\" + self.grillaCrucigrama)):
            archivo = open(self.vars["filesPath"].valor + "\\" +self.grillaCrucigrama,"w")
            archivo.close()

    def modificarCrucigrama(self):
        self.verArchivo(self.grillaCrucigrama)
        
    def cargarCrucigrama(self):
        self.crearGrilla()
        archivo = open(self.vars["filesPath"].valor + "\\" +self.grillaCrucigrama,"r")
        #cargo el crucigrama en la matriz self.grilla
        self.grilla = [ [letra for letra in fila if letra !="\n"] for fila in archivo.readlines()]
        archivo.close()
        
	#-----------------------
	#--- modificadores -----
	#-----------------------
	# Crear todos los modificadores con esta estructura, y SIEMPRE respetando el encabezado (self,key,*params):		
    def modifAlgunParametro(self,key,*params):
        #Modificador de una variable de usuario, 
        if(len(params) == 0):
            pass
			#realizar accion de modificacion, ejecutada cuando se hace a traves de interfaz.
        else:
			#realizar accion de modificacion, cuando se invoca programaticamente al metodo.
            pass
	#-----------------------
	#--- otros -------------	
	#-----------------------	
	#Este metodo muestra lo que quieras, la idea es que expliques como se usa el programa.
    def ayuda(self):
        print "-----------------------------------------------------------------"
        print "--- Crucigrammer ------------------------------------------------"
        print "-----------------------------------------------------------------"
        print "No estas cansado de no poder resolver esos dificiles crucigramas?\n"
        print "No busques mas, aca esta la solucion.\n"
        print "Carga el crucigrama, indicale las palabras a buscar, y listo\n"
        print "Crucigrammer encuentra las palabras por vos."
        print "No soportas la idea de armar vos mismo un crucigrama?\n"
        print "Aca esta la solucion, indicale las palabras, un ancho y alto"
        print "y listo! ya tenes tu crucigrama hecho. es muy dificil? no importa!"
        print "lee un poco mas arriba para encontrar la solucion a tu problema!"
	
    def funcionDeInicioLoop(self):
        self.mostrarGrilla(self.grilla)
        print "Palabras a buscar:"
        print self.palabras
        
	#Texto personalizado de salida.	
    def salirPrint(self):
        print "HASTAnbyq"
        print "hyLAcztqh"
        print "kiPROXIMA"

#esto siempre va.
# tenes que invocar a tu clase principal, los tres primeros parametros son el nombre, version y si es o no con pantalla grafica.
# despues tenes que pasarle todos los parametros que quieras, separados por comas.
if __name__ == '__main__':
	a = Crucigrammer("Crucigrammer","1.0.0",False,arg1="argumento1")
					
	a.menuPrincipal()		
