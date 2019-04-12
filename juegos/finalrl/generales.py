#-------------------  Imports  -------------------
#-------------------------------------------------
import os
import sys
sys.path.append('/home/luciano/python_scripts/matematica')
import matematica

#-------------------------------------------------
#----------------  Elegir Accion  ----------------
#-------------------------------------------------
# funcion para elegir una accion; toma como entrada un diccionario, 
# solicita la key a buscar, y si la encuentra, devuelve la key ingresada y valor en el diccionario.
def elegir_accion(diccionario):
	error = 1
	while(error == 1):
		key = matematica.convertir("string")
		try:
			error = 0
			instancia = diccionario[key]

		except(KeyError):
			print "Escribi bien Capo"
			error = 1

	return key, instancia

#-------------------------------------------------
#-------------  Calcular_cantidad  ---------------
#-------------------------------------------------
def calcular_cantidad(atacante,atacado,accion):
	cantidad = 0
	if (accion == "atacar"):
		cantidad = 5
	if (accion == "curar"):
		cantidad = 3

	return cantidad

#-------------------------------------------------
#---------------------  I. A. --------------------
#-------------------------------------------------
def inteligencia_artificial():
	pass
	return 0


