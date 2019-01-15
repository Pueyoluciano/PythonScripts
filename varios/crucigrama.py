import sys
sys.path.append('/home/luciano/python_scripts/matematica')
import matematica
import random

abcd = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
direcciones = {}
direcciones['1'] = [-1,1]
direcciones['2'] = [0,1]	
direcciones['3'] = [1,1]	
direcciones['4'] = [-1,0]	
direcciones['6'] = [1,0]
direcciones['7'] = [-1,-1]	
direcciones['8'] = [0,-1]	 	
direcciones['9'] = [1,-1]

class crucigrama():
	def __init__(self,letras,direcc):
		self.crucigrama =  []
		self.dimension = 0
		self.direcciones = direcc
		self.crear(letras)

	def crear(self,letras):
		print "alto&ancho:"
		self.dimension = matematica.convertir2('int',4,None,'')
		for i in range(0,self.dimension):
			aux = []
			for j in range(0,self.dimension):
				aux.append(random.choice(letras))
			self.crucigrama.append(aux)
		self.insertar()
		self.mostrar()

	def mostrar(self):
		for i in range(0,self.dimension):
			for j in range(0,self.dimension):
				print self.crucigrama[i][j],
			print ""

	def insertar(self):
		print "x:"
		print "--valores validos entre 1 y " + str(self.dimension) + " --"

		x = matematica.convertir2('int',1,self.dimension,'')
		# este x-1 lo hago para que cuando ingrese la poss,los indices vayan de 1 a tope y no de
		# 0 a tope-1 (como en el vector).
		x -= 1
		print "y:"
		print "--valores validos entre 1 y " + str(self.dimension) + " --"
		y = matematica.convertir2('int',0,self.dimension,'')
		y -= 1
		print "direccion:"
		direccion = matematica.convertir2('int',[1,2,3,4,6,7,8,9],None,'')
		print "palabra:"
		err = 1
		while (err == 1):	
			err = 0	
			palabra = matematica.convertir('string')
			a = x+(len(palabra)*self.direcciones[str(direccion)][0])
			b = y+(len(palabra)*self.direcciones[str(direccion)][1])
			if((a<0 or a >self.dimension) or (b<0 or b >self.dimension)):
				err = 1
		posx = x
		posy = y
		for i in range(0,len(palabra)):
			self.crucigrama[posy][posx] = palabra[i]
			posx+= self.direcciones[str(direccion)][0]
			posy+= self.direcciones[str(direccion)][1]

	def resolver(self):
		resultado = ''
		direccion = []
		print "palabra a buscar:"
		palabra = matematica.convertir('string')
		# recorro la sopa de letras
		for i in range(0,self.dimension-1):
			for j in range(0,self.dimension-1):
				# me muevo en caracol detectando coincidencia.
				# si hay mas de una, esta contemplado, se usa la lista "direccion"
				# se movera en todas las direcciones con coincidencia y verificara
				# en todas si hay conicidencia total.
				if (palabra[0] == self.crucigrama[i][j]):
					if(self.crucigrama[i][j+1] == palabra[1]):
						direccion.append(self.direcciones['6'])

					if(self.crucigrama[i-1][j+1] == palabra[1]):
						direccion.append(self.direcciones['9'])

					if(self.crucigrama[i-1][j] == palabra[1]):
						direccion.append(self.direcciones['8'])

					if(self.crucigrama[i-1][j-1] == palabra[1]):
						direccion.append(self.direcciones['7'])

					if(self.crucigrama[i][j-1] == palabra[1]):
						direccion.append(self.direcciones['4'])

					if(self.crucigrama[i+1][j-1] == palabra[1]):
						direccion.append(self.direcciones['1'])

					if(self.crucigrama[i+1][j] == palabra[1]):
						direccion.append(self.direcciones['2'])

					if(self.crucigrama[i+1][j+1] == palabra[1]):
						direccion.append(self.direcciones['3'])

					print direccion
					for k in range(0,len(direccion)):
						ok = 1
						posx = i + direccion[k][0]
						posy = j + direccion[k][1]
						for l in range(2,len(palabra)):
							if (palabra[l] != self.crucigrama[posy][posx]):
								ok = 0
								break
							else:
								posx += direccion[k][0]
								posy += direccion[k][1]
								resultado += self.crucigrama[posy][posx]
						if(ok == 1):
							print "encontrado"	
							print resultado	
					resultado = ''
					direccion = []
						



crusi = crucigrama(abcd,direcciones)
crusi.resolver()



















