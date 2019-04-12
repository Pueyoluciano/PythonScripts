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
# ------------------  imports  -------------------
#-------------------------------------------------

import pygame
import sys
import socket
import time
import os
pygame.mixer.init(frequency = 22050, size = -16, channels = 1, buffer = 4096)
pygame.mixer.music.set_volume(1)
pygame.init()

#-------------------------------------------------
# ------------  Sockets Servidor -----------------
#-------------------------------------------------

class gpio():
	def __init__(self):
		self.s = socket.socket()
		# setea el flag SO_REUSEADDR para que reutilice una coneccion abierta antes de que termine
		# el tiempo estandar para cerrarse por si sola.
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.s.bind(("localhost", 9999))
		self.s.listen(1)
		print "Esperando Cliente ..."
		self.sc, self.addr = self.s.accept()	
		
		# lee la entrada de datos(GPIO)
	def leer(self):
		self.dato1 = self.sc.recv(1024)
		self.dato2 = self.sc.recv(1024)
		print 'dato1: '+ self.dato1
		print 'dato2: '+ self.dato2
		if (self.dato1 != self.dato2):
			print memoria0.memoriabyte[self.dato1].nombre, memoria0.memoriabyte[self.dato2].reproducir()		

		return self.dato1, self.dato2
	
	def cerrar(self):
		self.sc.close()
		self.s.close()
			
#-------------------------------------------------
# -------------------  8bits  --------------------
#-------------------------------------------------

def binario(i):
	#Funcion que pasa de Decimal a Binario.
	byte = []
	aux = 0
	out = ''
	for j in range(0,8):
		aux = i%2
		i = int(i/2)
		byte.append(aux)
	byte.reverse()
	for j in range(0,8):
		out = out + str(byte[j])
	return out

#-------------------------------------------------
# ---------  Sacar el enter de un STR  -----------
#-------------------------------------------------

def sacarenter(palabra):
	palabra2 = ''
	for i in range(0,len(palabra)-1):	
		palabra2 += palabra[i]
	return palabra2

#-------------------------------------------------
# -------------------  PAD  ---------------------
#-------------------------------------------------

class pad():
	def __init__(self,codigo,nombre,sound0,sound1,sound2,sound3):
		self.codigo = codigo
		self.nombre = nombre
		if (sound0 != ""):
			self.sonido0 = pygame.mixer.Sound(sound0)
			self.sonido1 = pygame.mixer.Sound(sound1)
			self.sonido2 = pygame.mixer.Sound(sound2)
			self.sonido3 = pygame.mixer.Sound(sound3)
		else:
			self.sonido0 = ""
			self.sonido1 = ""
			self.sonido2 = ""
			self.sonido3 = ""

	def reproducir(self,volumen):
		# selecciona el sonido a reproducir en funcion del Volumen.
		if (volumen == 0):
			pass
		else:
			if (self.sonido0 != "sonido0"):
				if(volumen <=(1/16)*4):
					pygame.mixer.Sound.play(self.sonido0,1)
				else:
					if(volumen <= (1/16)*8):
						pygame.mixer.Sound.play(self.sonido1,1)	
					else:
						if(volumen <= (1/16)*12):
							pygame.mixer.Sound.play(self.sonido2,1)	
						else:
							pygame.mixer.Sound.play(self.sonido3,1)					

#-------------------------------------------------
# -------------------  PADS  ---------------------
#-------------------------------------------------

class banco():
	def __init__(self):
		# cpads = coleccion de pads
		self.cpads = {}

	def agregarpd(self,valor):
		num = 'PD'+ str(valor)
		dic = open("./dicciopadsdetalle") 
		flag = 0
		aux = ''
		while (1 == 1):
			aux = sacarenter(dic.readline())

			if (aux[0] != '@'):
				if (aux == num):
					flag = 1
					nombre = sacarenter(dic.readline())
					sonido0 = sacarenter(dic.readline())
					sonido1 = sacarenter(dic.readline())
					sonido2 = sacarenter(dic.readline())
					sonido3 = sacarenter(dic.readline())
				else:
					pass
			else:
				break
		dic.close()
		if (flag == 1):
			self.cpads[num] = pad(num,nombre,sonido0,sonido1,sonido2,sonido3)
		else:
			self.cpads[num] = pad(num,num,"sonido0","sonido1","sonido2","sonido3")
		print self.cpads[num].nombre
		return self.cpads[num]		

#-------------------------------------------------
# -------------  PALABRA RESERVADA  --------------
#-------------------------------------------------

class palabra():
	def __init__(self,nombre):
		self.nombre = nombre

	def reproducir(self):
		print self.nombre

#-------------------------------------------------
# ------------  PALABRAS RESERVADAS  -------------
#-------------------------------------------------

class palres():
	def __init__(self):
		self.prs = {}

	def agregarpr(self,valor):
		num = 'PR' + str(valor)
		self.prs[num] = palabra('palabra reservada ' + str(valor))
		return self.prs[num]

#-------------------------------------------------
# --------------  NIVEL DE VOLUMEN  --------------
#-------------------------------------------------

class volumen():
	def __init__(self,val):
		self.val = val

	def reproducir(self):
		return self.val

#-------------------------------------------------
# -------------  NIVELES DE VOLUMEN  -------------
#-------------------------------------------------

class volumenes():
	def __init__(self):
		self.nvs = {}
		
	def agregarnv(self,valor):
		num = 'NV' + str(valor)	
		self.nvs[num] = volumen(0.0625 + (0.0625 * len(self.nvs)))
		return self.nvs[num]
		
#-------------------------------------------------
# -------  Llenar memoria con el archivo  --------
#-------------------------------------------------

class memoria():
	def __init__(self):
		# Ej: {'00000000': 'PR00'}
		self.memoriabyte = {}

	def iniciarmemoria(self):
		# dicciomemoriadetalle es el txt de donde levanta la info
		diccio = open("./dicciomemoriadetalle")
		while (1 == 1):
			i = 0
			tipo = ''
			valor = ''
			pos = ''
			auxiliar = diccio.readline()
			# @ caracter de fin de archivo (PORQUE NO SE COMO HACER QUE LO DETECTE SOLO)
			if (auxiliar[0] == '@'):
				break
			else:
			# los primeros 8 caracteres son los 8 bits que representan la memoria (ver dicciomemoriadetalle) 
				for i in range(0,8):
					pos = pos+ str(auxiliar[i])
				i = i + 1 
				while (auxiliar[i] != '\n'):
					# con '\n' busca hasta el fin del renglon	
				 	# si es el caracter ':', lo ignora
					# los primeros dos caracteres despues del ':' son el tipo: PR,NV,PD,-- 
					# -- "PR": Palabra Reservada
					# -- "NV": Nivel de Volumen
					# -- "PD": Pad
					# -- "--": no asignado
					# los ultimos 2 caracteres son el numero del tipo, 00, 10, 15 ...

					if (auxiliar[i] != ':'):
						if (len(tipo) < 2):
							tipo = tipo + str(auxiliar[i])
						else:
							valor = valor + str(auxiliar[i])
					i = i + 1

					# dependiendo del Tipo, se agrega un nuevo, pad, nivel de Vol, o palabra reservada.
					# llamando al metodo de la clase correspondiente.
					# si encuentra "--" u otra cosa rara llena la posicion con '----'
				if (tipo == 'PR'):
					self.memoriabyte[pos] = palares.agregarpr(valor)
				if (tipo == 'NV'):
					self.memoriabyte[pos] = volumenes0.agregarnv(valor)
				if (tipo == 'PD'):
					self.memoriabyte[pos] = banco0.agregarpd(valor)
				if (tipo == '--'):
					self.memoriabyte[pos] = '----'
				if (tipo != 'PR' and tipo != 'NV' and tipo != 'PD' and tipo != '--'):
					self.memoriabyte[pos] = '----'				
		diccio.close()

	def leergpio(self,dat1,dat2):
		# Si dato 1 y 2 son iguales es una palabra reservada, entonces solo llama al .reproducir
		# de esa palabra reservada.
		# Si son distintos entonces es un PAD y un VOLUMEN en ese orden, entonces llama al
		# .reproducir del PAD, y toma como parametro el .reproducir del VOLUMEN, que devuelve
		# el Float correspondiente a la muestra tomada. (EJ: 0.0625)

		if (dat1 == dat2):
			memoria0.memoriabyte[dat1].reproducir()
		else:
			memoria0.memoriabyte[dat1].reproducir(memoria0.memoriabyte[dat2].reproducir())
	
#---palares = palabras reservadas
#---volumen = niveles de vol.
#---banco = guarda los Pads

volumenes0 = volumenes()
palares = palres()
banco0 = banco()
memoria0 = memoria()
memoria0.iniciarmemoria()

#for i in range(0,256):
#	print binario(i), memoria0.memoriabyte[binario(i)] 	

socket0 = gpio()

#print banco0.cpads['PD00'].sonido0
#print palares.prs['PR00']
#print volumenes0.nvs['NV00']

#-------------------------------------------------
# --------------------  Screen  ------------------
#-------------------------------------------------

def pantalla():
	os.system("clear")
	print "---------------------------------------------"
	print "()       -------- RB.PI V1.0 -------       ()" 
	print "---------------------------------------------"
	
#-------------------------------------------------
# --------------------- Main  --------------------
#-------------------------------------------------

pantalla()
while (1 == 1):

	dat1,dat2 = socket0.leer()
	if((dat1 == '00000000' or dat2 == '00000000') or (dat1 == '' or dat2== '')):
		break	
	else:
		memoria0.leergpio(dat1,dat2)

socket0.cerrar()








