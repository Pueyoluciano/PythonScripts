import os
import Aplicacion
import math
import random
from datetime import datetime
from Menu import *
from Variable import *

class Prueba(Aplicacion.Aplicacion):
	def iniciar(self,**args):	
		# las variables de usuario se agregan con la clase Variable.
		# la funcion para modificarlas debe ser creada en la clase que hereda de Aplicacion (En este caso NombreClase)
		self.vars["var1"] = Variable(args["param1"],self.modifGenerico,0,5,flag1=True) 

		 # para agregar items al menu, crear la estructura de Nodos que se queira ,luego llamar agregarMenu(indice del menu,Nodo)
		leaf1 = Leaf("","",self.generar)
		self.agregarMenu(0,leaf1)

		# Aqui se agregan las postFunciones.
		# Las post funciones son aquellas que se ejecutan (siempre) luego de realizar una modificacion.
		self.agregarPostFunciones(self.postFuncion1):
		
	# las funciones modificadoras deben tener la forma nombre(self,Key):	
	def modifVar1(self,key):
		self.vars["var1"].valor = validador.ingresar(int,validador.entre,self.vars["var1"].minimo,self.vars["var1"].maximo)
	
	# las post funciones son aquellas que se ejecutan (siempre) luego de realizar una modificacion.
	def postFuncion1(self):
		pass
	
# esta parte es para ejecutar el archivo.py como un exe y que abra el menu.		
if __name__ == '__main__':	
	a = Prueba("NombreAPP","Version",False,param1=1,param2=2)
	a.menuPrincipal()		