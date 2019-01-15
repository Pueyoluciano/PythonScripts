import os
import random

usuarios = [["Jose",0],["Luciano",0],["Gabriel",0],["Sebastian",0]]
#Paises O Aplicaciones
poa = [["Chile",0],["Colombia",0],["Espana",0],["Peru",0],["Brasil",0],["ANS(Chile)",0],["ANS(Brasil)",0]]

hh =[["jose",]]
#cantidad de usuarios
cusuarios = len(usuarios)
aleatorio = []

def cargahoras():
	suma = 0.0
	for i in range(0,len(poa)):
		os.system("clear")
		print poa[i][0]
		poa[i][1] = float(raw_input("horas:"))
		suma+=poa[i][1]
	return suma

def rand():
	for i in range(0,cusuarios):
		if (len(aleatorio) != 0):
			correcto = 0
			while (correcto != 1):
				aux3 = int(random.random()*cusuarios)
				for j in range(0,len(aleatorio)):
					if (aleatorio[j] == aux3):
						correcto = 0		
						break
					else: 		
						correcto = 1
			aleatorio.append(aux3)
		else:
			aleatorio.append(int(random.random()*cusuarios))
	print aleatorio


def cargahorasf():
	parcial = suma/0.5
	while (parcial != 0):
		for i in range(0,cusuarios):
			if (parcial != 0):
				usuarios[aleatorio[i]][1] += 0.5
				parcial -= 1
			else:
				break

suma = cargahoras()
rand()
cargahorasf()

#os.system("clear")
print usuarios
print poa









