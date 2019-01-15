import socket
import time
import os
#-------------------------------------------------
# ------------------ graficador ------------------
#-------------------------------------------------

def dibujar(tate):
#	a = "___|___|___"
#	b = "___|___|___"
#	c = "   |   |   "
#   partidas: X
#   jugador1: X
#   jugador2: X
	a = ""
	b = ""
	c = ""
	d = [a,b,c]
	x = ""
	y = ""
	z = ""
	e = [x,y,z]
	os.system("clear")
	for i in range(0,3):
		for j in range(0,3):
			if(tate[i][j] == 0):
				if (i<2):
					e[j] = "_"
				else:
					e[j] = " "
				continue
			if(tate[i][j] == 1):
				e[j] = "X"
				continue
			if(tate[i][j] == 2):
				e[j] = "O"
				continue
		if (i<2):
			d[i] = ("_"+e[0]+"_|_"+e[1]+"_|_"+e[2]+"_")
		else:
			d[i] = (" "+e[0]+" | "+e[1]+" | "+e[2]+" ")			

	print "-- Jugador 2 --"
	print ""
	print "partidas:  " + str(partidas)
	print "Jugador 2: " + str(jdos)
	print "Jugador 1: " + str(juno)
	print ""
	for i in range(0,len(d)):
		print d[i]

	return d

#-------------------------------------------------
# ------------- funcion para ganador -------------
#-------------------------------------------------

def gano(tate,jugador):
	ganado =  0
	sol = 0
#	gan = [[1,0,0],[1,0,0],[1,0,0]]
	if (tate[0][0] == jugador and tate[1][0] == jugador and tate[2][0] == jugador ):
		ganado = jugador
		sol = 1

#	gan = [[0,1,0],[0,1,0],[0,1,0]]
	if (tate[0][1] == jugador and tate[1][1] == jugador and tate[2][1] == jugador ):
		ganado = jugador
		sol = 1

#	gan = [[0,0,1],[0,0,1],[0,0,1]]
	if (tate[0][2] == jugador and tate[1][2] == jugador and tate[2][2] == jugador ):
		ganado = jugador
		sol = 1

#	gan = [[1,1,1],[0,0,0],[0,0,0]]
	if (tate[0][0] == jugador and tate[0][1] == jugador and tate[0][2] == jugador ):
		ganado = jugador
		sol = 1


#	gan = [[0,0,0],[1,1,1],[0,0,0]]
	if (tate[1][0] == jugador and tate[1][1] == jugador and tate[1][2] == jugador ):
		ganado = jugador
		sol = 1

#	gan = [[0,0,0],[0,0,0],[1,1,1]]
	if (tate[2][0] == jugador and tate[2][1] == jugador and tate[2][2] == jugador ):
		ganado = jugador
		sol = 1

#	gan = [[1,0,0],[0,1,0],[1,0,0]]
	if (tate[0][0] == jugador and tate[1][1] == jugador and tate[2][2] == jugador ):
		ganado = jugador
		sol = 1

#	gan = [[0,0,1],[0,1,0],[1,0,0]]
	if (tate[0][2] == jugador and tate[1][1] == jugador and tate[2][0] == jugador ):
		ganado = jugador
		sol = 1

	if (sol == 1):
		print "El jugador "+str(jugador)+" Gana"
		raw_input("[...]")

	return ganado

#-------------------------------------------------
# -------------------- Enviar --------------------
#-------------------------------------------------

def enviar(dato,c):
	c.send(str(dato))


#-------------------------------------------------
# ------------------- Recibir --------------------
#-------------------------------------------------

def recibir(c):
	dato = c.recv(1024)
	return dato

#-------------------------------------------------
# ---------------- recibir listas ----------------
#-------------------------------------------------

def recibirtat(aux):
	tate= [[0,0,0],[0,0,0],[0,0,0]]
	cont = 0
	for i in range(0,3):
		for j in range(0,3):
			tate[i][j] = int(aux[cont])
			cont += 1
	return tate

#-------------------------------------------------
# ----------------- enviar listas ----------------
#-------------------------------------------------

def enviartat(tate):
	aux = ""
	for i in range(0,3):
		for j in range(0,3):
			aux += str(tate[i][j])
	return aux

#-------------------------------------------------
# ------------------- Jugador 1 ------------------
#-------------------------------------------------

def juegauno(tate,c):
	tate = recibirtat(recibir(c))
	
	ganador = gano(tate,1)
	dibujar(tate)
	return ganador

#-------------------------------------------------
# ------------------- Jugador 2 ------------------
#-------------------------------------------------

def juegados(tate,c):

	tate = recibirtat(recibir(c))
	dibujar(tate)
	aux2 = 0
	while (aux2 == 0):
		pos = raw_input("> ")
		if (len(pos) == 1):
			if (pos.isdigit()):
				if(pos > 0):
					for i in range(0,3):
						for j in range(0,3):	
							if (pad[i][j] == int(pos)):
								if (tate[i][j] == 0):
									tate[i][j] = 2 
									aux2 = 1
									break 
								else:
									aux2 = 0
	enviar(enviartat(tate),c)
	dibujar(tate)
	ganador = gano(tate,2)
	return ganador

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------

#-------------------------------------------------
# ------------------- Programa -------------------
#-------------------------------------------------

pad = [[7,8,9],[4,5,6],[1,2,3]]
tat= [[0,0,0],[0,0,0],[0,0,0]]
pos = 0
aux = 0
ganador = 0

c = socket.socket()
c.connect(("localhost", 9999))
os.system("clear")
print "..."
while (1 == 1):
	partidas = int(recibir(c))
	juno = int(recibir(c))
	jdos = int(recibir(c))

	dibujar(tat)

	if (partidas%2 == 0):
		while (ganador == 0):
			ganador = juegauno(tat,c)

			if (ganador == 0):
				ganador = juegados(tat,c)
	else:
		while (ganador == 0):
			ganador = juegados(tat,c)

			if (ganador == 0):
				ganador = juegauno(tat,c)
	
	if (ganador == 1):
		print "El jugador 1 Gana"
		raw_input("[...]")
	else:
		print "El jugador 1 Gana"
		raw_input("[...]")

c.close()

