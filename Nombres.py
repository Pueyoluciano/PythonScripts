import random
import Aplicacion
import Reglas
from Menu import *
from Variable import *
from validador import *
#------------------------------------------------
#--------------- TODO ---------------------------
#------------------------------------------------


#------------------------------------------------
#------------------------------------------------
#------------------------------------------------
class CreadorNombres(Aplicacion.Aplicacion):
	def iniciar(self,**args):	
		#variables de programa
		self.vocales = set(["a","e","i","o","u"])
		self.consonantes = set(["b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","y","z"])
		self.letras = self.vocales.union(self.consonantes)
		self.listado = Reglas.ListadoReglas.contenido
		
		self.reglasActuales = ["unaConsontanteHastaDosVocales","qSiempreConU","quSiempreConEI"]
		
		self.motor = Reglas.MotorReglas()
		self.motor.agregarReglas([self.listado.obtenerItem(regla) for regla in self.reglasActuales])
		
		#variables de usuario	
		self.vars["longitud"] = Variable(5,self.modifGenerico,minimo=0,maximo=20,orden=0)

		#Items del Menu
		self.agregarMenu(0,Leaf("Crear nombre","Genera un nombre aleatorio en base a las reglas seteadas",self.crearNombre))
		self.agregarMenu(1,Leaf("Ver reglas","Listar reglas vigentes",self.verTodasReglas))
		self.agregarMenu(2,Leaf("Modificar reglas","agregar/quitar reglas para la generacion de nombres",self.modifReglas))
		
		#Funciones que se ejecutan luego de llamar a Modificar.
		#self.agregarPostFunciones()

	def crearNombre(self):
		seguir = True
		while(seguir):
			#Elijo la primera letra
			nombre = random.sample(self.letras,1)[0].upper()
			
			#Si la Longitud es 0 elije una longitud Random
			if (self.vars["longitud"].valor == 0):
				longitud = random.randint(self.vars["longitud"].minimo,self.vars["longitud"].maximo)
			else:
				longitud = self.vars["longitud"].valor
			
			#Genero todo el nombre
			for i in range(0,longitud-1):
				nombre += self.motor.nuevaLetra(nombre.lower())			
				
			print "-> " + nombre
			print "otro nombre?"
			seguir = validador.ingresarSINO()

	def verTodasReglas(self):
		self.espaciador()
		i = 1	
		for regla in self.listado.contenido:
			print str(i) + ") [" + str("x" if (regla.nombre in self.reglasActuales) else " ") + "] " + regla.nombre
			i+=1		
		self.espaciador()	

	def verReglas(self,reglasTemporal):	
		i = 1	
		for regla in self.listado.contenido:
			print str(i) + ") [" + str("x" if (regla.nombre in reglasTemporal) else " ") + "] " + regla.nombre
			i+=1	
		
	def modifReglas(self):
		self.espaciador()
		listaTemp = self.reglasActuales[:]
		seguir = True
		
		while(seguir):

			self.verReglas(listaTemp)
			print str(len(self.listado.contenido) + 1) + ") Confirmar"
			print str(len(self.listado.contenido) + 2) + ") Volver"
			self.espaciador()
			
			respuesta = validador.seleccionar([regla.nombre for regla in self.listado.contenido] +["confirmar"] + ["volver"])
			if(respuesta != "volver"):
				if(respuesta != "confirmar"):
					if(respuesta in listaTemp):
						listaTemp.remove(respuesta)
					else:
						listaTemp.append(respuesta)
						
				else:
					self.reglasActuales = listaTemp[:]
					self.motor.limpiarReglas()
					self.motor.agregarReglas([self.listado.obtenerItem(regla) for regla in self.reglasActuales])
					seguir = False
			else:		
				seguir = False
				
		self.espaciador()
		
	def ayuda(self):
		self.espaciador()
		print "FILL ME"
		self.espaciador()
	
	#Texto personalizado de salida.	
	def salirPrint(self):
		print "----"

if __name__ == '__main__':
	a = CreadorNombres("CreadorDeNombres","1.0.0",False)
					
	a.menuPrincipal()		
