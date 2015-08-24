import pygame
import Funcionesfractales as ff
import multiprocessing as mp

def convertirPC(x,y,deltax,deltay,xmin,ymin): # convertir de pixel a complejo
	equis = xmin + (x * deltax)
	ygrie = ymin + (y * deltay)
	
	return complex(equis,ygrie)		
	
def funcionParalela(mandelbrot,alto,desdex,hastax,planoComplejo,resolucion,norma):
	pantallaPixeles = []
	for x in range(desdex,hastax):
		pantallaPixeles.append([])
		for y in range(0,alto):
			valor = mandelbrot.calcular(planoComplejo[x][y],[resolucion,norma])
			pantallaPixeles[x-desdex].append([valor,valor,valor])
	
	return pantallaPixeles

if __name__ == '__main__':   
	pygame.init()
	ancho = 20
	alto = 20
	screen = pygame.display.set_mode((ancho,alto))
	pixelArray = pygame.PixelArray(screen)
	resolucion = 50
	norma = 2.0
	funciones = ff.Funciones()
	mandelbrot = funciones.obtenerFuncion("mandelbrot")

	xmin   = -4
	xmax   = 4
	ymin   = -4
	ymax   = 4

	deltax = abs(xmin - xmax) / (float(ancho) - 1)
	deltay = abs(ymin - ymax) / (float(alto) - 1)

	planoComplejo = []
	pantallaPixeles = []
			
	for x in range(0,ancho):	
		planoComplejo.append([])
		pantallaPixeles.append([])
		for y in range(0,alto):
			planoComplejo[x].append(convertirPC(x,y,deltax,deltay,xmin,ymin))
			
	pool = mp.Pool(processes=4)
	results = [pool.apply(funcionParalela, args=(mandelbrot, alto, 0 + (5*x) , 5 + (5*x), planoComplejo, 50, 2)) for x in range(0,4)]
	results = results[0] +  results[1] +  results[2] +  results[3]
	print results
	
	pygame.surfarray.blit_array(sreen,results)
