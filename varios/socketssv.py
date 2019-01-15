#Servidor.
import socket
import time
import os

#---SERVIRDOR ---
#s = socket.socket()
#s.bind(("localhost", 9999))
#s.listen(1)
#while True:
#	recibido = sc.recv(1024)
#	if recibido == "quit":
#		break
#	print "Recibido:", recibido
#	sc.send(recibido)

#print "adios"
#sc.close()
#s.close()

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
	
	print "-- Jugador 1 --"
	print ""
	print "partidas:  " + str(partidas)
	print "Jugador 1: " + str(juno)
	print "Jugador 2: " + str(jdos)
	print ""
	for i in range(0,len(d)):
		print d[i]

	return d

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
# -------------------- Enviar --------------------
#-------------------------------------------------

def enviar(dato,sc):
	sc.send(str(dato))
	time.sleep(1)

#-------------------------------------------------
# ------------------- Recibir --------------------
#-------------------------------------------------

def recibir(sc):
	dato = sc.recv(1024)
	time.sleep(1)
	return dato

#-------------------------------------------------
# ------------------- Jugador 1 ------------------
#-------------------------------------------------

def juegauno(tate,sc):
	dibujar(tate)
	pos = 0
	aux = 0
	while (aux == 0):
		pos = raw_input("> ")
		if (len(pos) == 1):
			if (pos.isdigit()):
				if(pos > 0):
					for i in range(0,3):
						for j in range(0,3):	
							if (pad[i][j] == int(pos)):
								if (tate[i][j] == 0):
									tate[i][j] = 1 
									print aux
									aux = 1
									break 
								else:
									aux = 0

	dibujar(tate)
	enviar(enviartat(tate),sc)
	ganador = gano(tate,1)	
	return tate,ganador

#-------------------------------------------------
# ------------------- Jugador 2 ------------------
#-------------------------------------------------

def juegados(tate,sc):
	enviar(enviartat(tate),sc)

	tate = recibirtat(recibir(sc))
	dibujar(tate)
	ganador = gano(tate,2)
	return tate,ganador


#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------

#-------------------------------------------------
# ------------- variables de programa ------------
#-------------------------------------------------

# jugador 1 = X /en tat: 1
# jugador 2 = O /en tat: 2
pad = [[7,8,9],[4,5,6],[1,2,3]]
tat = [[0,0,0],[0,0,0],[0,0,0]]
salir = 0 
juno = 0
jdos = 0
ganador = 0
partidas = 0

#-------------------------------------------------
# -------------- inicializa sockets --------------
#-------------------------------------------------

s = socket.socket()
s.bind(("localhost", 9999))
s.listen(1)

os.system("clear")
print "-------------------------------------------------"
print "-------------------  tei tou ti -----------------"
print "-------------------------------------------------"
print " se juega con el pad numerico."
print " prohibido hablar del club de la pelea."
print "-------------------------------------------------"
print "-------------------------------------------------"
print ""
print "Esperando Cliente.."
sc, addr = s.accept()
os.system("clear")
print "..."

#-------------------------------------------------
# ------- partidas pares empieza jugador 1 -------
#-------------------------------------------------

while (1 == 1):
	ganador = 0
	enviar(partidas,sc)
	enviar(juno,sc)
	enviar(jdos,sc)

	if (partidas%2 == 0):
		while(ganador == 0):
			tat,ganador = juegauno(tat,sc)

			if (ganador == 0):
				tat,ganador = juegados(tat,sc)

#-------------------------------------------------
# ------ partidas impares empieza jugador 2 ------
#-------------------------------------------------

	else:
		while(ganador == 0):
			tat,ganador = juegados(tat,sc)

			if (ganador == 0):
				tat,ganador = juegauno(tat)

	if (ganador == 1):
		juno += 1
	else:
		jdos += 1
	for i in range (0,3):	
		for j in range(0,3):
			tat[i][j] = 0
	partidas += 1

sc.close()
s.close()


