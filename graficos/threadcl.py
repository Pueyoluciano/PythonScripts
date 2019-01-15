import socket
import os
import threading
import time
import string

#-------------------------------------------------
# -------------------- Enviar --------------------
#-------------------------------------------------

def enviar(s):
	salir = 0
	dato = raw_input('> ')
	s.send(str(dato))
	if (dato == 'salir'):
		salir = 1

	return dato,salir

#-------------------------------------------------
# ------------------- Recibir --------------------
#-------------------------------------------------

def recibir(s):
	salir = 0
	dato = s.recv(1024)
	print dato
	if (dato == 'salir'):
		salir = 1
	return dato,salir

#-------------------------------------------------
# ------------------ Conectarse ------------------
#-------------------------------------------------

s = socket.socket()
s.connect(('localhost', 9999))
os.system('clear')

#-------------------------------------------------
#--------------- Thread Recibe -------------------
#-------------------------------------------------	

class recibirth(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		self.salir = 0	
		self.dato = ''
		while (self.salir == 0):
			self.dato,self.salir = recibir(s)
		print 'adios'	

#-------------------------------------------------
#---------------- Thread Envia -------------------
#-------------------------------------------------

class enviarth(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		self.salir = 0	
		self.dato = ''
		while (self.salir == 0):
			self.dato,self.salir = enviar(s)
		print 'adios'	
	
recibir(s)
enviar(s)	

a = recibirth()
a.start()
b = enviarth()
b.start()
#a.join()
#b.join()


s.close()
