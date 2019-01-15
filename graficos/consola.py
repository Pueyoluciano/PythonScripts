import os

os.system("clear")

def crearmapa():
	mapp = []
	print "Filas: "
	filas = raw_input("> ")
	print "Columnas: "
	columnas = raw_input("> ")
	for i in range(0,int(filas)):
		mapp.append([])	
		for j in range(0,int(columnas)):
			mapp[i].append(0)
	return mapp

def mostrarmapa(mapa):
	cero = "."
	uno = "@"
	largo = len(mapa)
	alto = len (mapa[0])
	for i in range(0,largo):
		for j in range(0,alto):
			if(mapa[i][j] == 0):
				print cero,
			if(mapa[i][j] == 1):
				print uno,
		print ""

mapa = crearmapa()

mapa[0][2] = 1

mostrarmapa(mapa)




