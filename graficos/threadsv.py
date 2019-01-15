import socket
import os
import threading
import time
import string

#-------------------------------------------------
#--------------------- Enviar --------------------
#-------------------------------------------------

def enviar(c):
	salir = 0
	dato = raw_input('> ')
	c.send(str(dato))
	if (dato == 'salir'):
		salir = 1
	
	return dato,salir

#-------------------------------------------------
#-------------------- Recibir --------------------
#-------------------------------------------------

def recibir(c):
	salir = 0
	dato = c.recv(1024)
	print dato
	if (dato == 'salir'):
		salir = 1
	return dato,salir

#-------------------------------------------------
#-------------- iniciar socket -------------------
#-------------------------------------------------

def iniciarsocket(hostname,port,listen):
	s = socket.socket()
	s.bind((hostname, port))
	s.listen(listen)
	print 'Esperando al cliente (...) '
	c, addr = s.accept()
	os.system('clear')
	return s,c

s,c = iniciarsocket('localhost',9999,1)

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
			self.dato,self.salir = recibir(c)
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
			self.dato,self.salir = enviar(c)
		print 'adios'	


enviar(c)
recibir(c)
		
a = recibirth()
a.start()
b = enviarth()
b.start()
#a.join()
#b.join()

c.close()
s.close()










