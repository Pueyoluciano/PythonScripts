import socket
import time
import os

c = socket.socket()
c.connect(("localhost", 9999))

#-------------------------------------------------
# -------------------- Enviar --------------------
#-------------------------------------------------

def enviar(dato,c):
	c.send(str(dato))

#-------------------------------------------------
# ------------------- Recibir --------------------
#-------------------------------------------------

#def recibir(c):
#	dato = c.recv(1024)
#	return dato

class bateria():
	def enviarbyte(self):
		enviar('11110000',c)


while (1 == 1):
	entrada = raw_input("> ")
	if (entrada == 'salir' or entrada == '0'):
		break
	else:
		if (len(entrada) != 8):
			enviar('00000000',c)
		else:
			if (entrada == '0'):
				enviar(entrada,c)
				break
			else:
				enviar(entrada,c)

c.close()
