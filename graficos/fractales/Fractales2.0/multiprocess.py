#http://pymotw.com/2/multiprocessing/basics.html

import multiprocessing as mp

def f(q):
	q.put(6)

if __name__ == '__main__':
	q = mp.Queue()
	p = mp.Process(target=f,args=(q,))
	p.start()
	p.join()
	print q.get()
	
class graficador:
	def __init__(self,ancho,alto,xmin,xmax,ymin,ymax,funcion,parametros,paleta):
		self.ancho = ancho
		self.alto = alto
		self.xmin = xmin
		self.xmax = xmax
		self.ymin = ymin
		self.ymax = ymax
		self.funcion = funcion
		self.parametros = parametros
		self.paleta = paleta
		
	def convertirPC(self,x,y): # convertir de pixel a complejo
		equis = self.xmin + (x * (abs(self.xmin - self.xmax) / (float(self.ancho) - 1)))
		ygrie = self.ymin + (y * (abs(self.ymin - self.ymax) / (float(self.alto) - 1)))		
		return complex(equis,ygrie)
		
	def graficar(self,desde,hasta,queue):
		#queue tiene el pixelarray adentro
		#desde = (xi,yi)
		#hasta = (xf,yf)	
		for x in range(desde[0],hasta[0]):
			for y in range(desde[1],hasta[1]):
				complejo = self.convertirPC(x,y)
				valor = funcion.calcular(complejo,self.parametros)
				color = self.paleta.grilla[valor-1]
				queue.get()[x,y] = color
		
		return self.pxarray
					
					
					
					
					
					
					
					
					
					