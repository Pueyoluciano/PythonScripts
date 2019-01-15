import os

yyy = 2

xxx = 2

matrizz=[[0.0,0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0]]

#----------------------------------------- MENU ---------------------------------------------------------

def main(yyy,xxx):
	while 1 == 1:	
		os.system("clear") 		
		print "---------------------------------Matrices V1.0---------------------------------\n"
		print "---------Opciones--------\n\n1)Pasar numero a fraccion\n2)Dimension de la matriz\n3)Salir\n"		
		resp = str(raw_input(":"))		
		if str(resp) == "1":
			numero = raw_input("(ingrese un numero en forma decimal): ")			
			numero2 = pasarafraccion(numero)
			print numero2
			raw_input("...")				
		if str(resp) == "2":
			os.system("clear")
			print "---------------------------------Matrices V1.0---------------------------------\n"
			print "MATRICES DE HASTA 7x7"				
			try:
				yaux=int(raw_input("filas:"))
			except ValueError:
				yaux = 2				
				print "Valor no numerico"
				raw_input("...")	
			try:
				xaux=int(raw_input("columnas:"))
			except ValueError:
				xaux = 2				
				print "Valor no numerico"
				raw_input("...")			
			if (xaux<=7 and xaux>=1)and (yaux<=7 and yaux>=1):
				yyy = yaux
				xxx = xaux
			else:
				print "Exede rango permitido"
				yyy=2
				xxx=2				
			limpiarmatriz(matrizz,yyy,xxx)								
			main2x2(yyy,xxx)			
		if str(resp) == "3":
			os.system("clear")				
			break

#-------------------------------------------MATRIZ ------------------------------------------------

#-------- MENU MATRIZ ----------		

def main2x2(yyy,xxx):
	while 1 == 1:
		os.system("clear") 		
		print "---------------------------------Matrices V1.0---------------------------------\n"		
		print"------Menu "+str(yyy)+"x"+str(xxx)+" ------\n\n1)Mostrar la matriz\n2)Cargar la matriz\n3)Reordenar la matriz\n4)limpiar la matriz\n5)Resolver matriz\n6)Volver"
		resp = raw_input(":")	
		try:	
			if int(resp) == 1:
				mostrarmatriz(matrizz,yyy,xxx)
			if int(resp) == 2:
				cargarmatriz(matrizz,yyy,xxx)
			if int(resp) == 3:
				mostrarmatriz(matrizz,yyy,xxx)
				acomodar(matrizz,yyy,xxx)
				mostrarmatriz(matrizz,yyy,xxx)				
			if int(resp) == 4:
				limpiarmatriz(matrizz,yyy,xxx)				
			if int(resp) == 5:								
				resolvermatriz(matrizz,yyy,xxx)	
			if int(resp) == 6:
				break	
		except ValueError:
			print "Valor no numerico"
			raw_input("...")

#-------- MOSTRAR MATRIZ ----------

def mostrarmatriz(matrizz,yyy,xxx):
	print "\n"	
	for i in range (0,int(yyy)):
		for j in range (0,int(xxx)):	
			num = pasarafraccion(matrizz[i][j])
			print str(num)+"  ",
		print"\n"	
	raw_input("Presione ENTER para continuar...")		
	os.system("clear")	

#-------- RESOLVER LA MATRIZ(GAUSS) ----------

def resolvermatriz(matrizz,yyy,xxx):
	matrizr=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,] #matriz de resolucion.
	if yyy <=7 and xxx<=7 :
		asd = str(raw_input("Ver Paso a Paso?(1/0)"))		
		if str(asd) == "1" or str(asd) == "y" or str(asd) == "Y" or str(asd) == "s" or str(asd) == "S":
			asd = 1
		else:
			asd = 0
		mostrarmatriz(matrizz,yyy,xxx)		
		for n in range(0,(xxx-1)):# n:cant. de veces que te corres a la derecha			
			acomodar(matrizz,yyy,xxx)		
			for h in range(n,xxx):			
				matrizr[h]=matrizz[h][n]#carga la matriz de resol desde la diagonal hacia abajo			
			for i in range((n+1),xxx):		
				for j in range (n,xxx):			
					if matrizr[n]!=0: #para evitar x/0.						
						x=matrizr[i]/matrizr[n]				
						matrizz[i][j]=matrizz[i][j] - (matrizz[n][j]*x)					
					if asd == 1:					
						mostrarmatriz(matrizz,yyy,xxx)
						os.system("clear")
		if asd == 0:
			mostrarmatriz(matrizz,yyy,xxx)

#-------- ACOMODAR LA MATRIZ ----------

def acomodar(matrizz,yyy,xxx):
	vector = [0,0,0,0,0,0,0]# vector que carga cantidad de 0 por fila.
	mm = 0 # mm es el flag para indicar que esta acomodado.
	while int(mm) == 0:
		vector = [0,0,0,0,0,0,0]
		mm = 1		
		for i in range(0,yyy):# este primer ciclo for carga el vector comentado arriba.
			for j in range(0,xxx):
				if matrizz[i][j] == 0:
					vector[i]=vector[i]+1		
		
		for i in range (0,yyy-1): # burbujeo divertido
			for j in range(1,yyy-i):
				asd = yyy-j				
			if asd < 0:
				asd= asd * (-1)
			if vector[i] > vector[asd]:								
				mm = 0				
				for k in range(0,xxx):# swap		
					aux = matrizz[i][k]
					matrizz[i][k] = matrizz[asd][k]
					matrizz[asd][k] = aux		
	
#-------- CARGAR LA MATRIZ ----------

def cargarmatriz(matrizz,yyy,xxx):
	entero = ""
	coma = ""
	flag = 0	
	ci = 0 # Caracter Incorrecto    // ambos para detectar caracteres incorrectos en el ingreso de datos
	cp = 0 # Caracter coma
	for i in range (0,int(yyy)):
		for j in range (0,int(xxx)):
				os.system("clear")
				print str(i)+" "+str(j)+":\n"	
				for k in range (0,int(yyy)):
					for l in range (0,int(xxx)):	
						num = pasarafraccion(matrizz[k][l])
						if i == k and j== l:
							print "_  ",
						else:
							print str(num)+"  ",
					print"\n"#-------------------------------------Hasta aca es para visualizar					
				aux = raw_input(":")
				ci = 0
				cp = 0				
				for w in aux:
					if cp == 0:						
						if w.isdigit()== True or (w =="." or w == "-"):
							if w == ".": 									
								cp = 1
						else:
							ci = 1
							break
					else:
						if w.isdigit()== False:
							ci = 1
							break					
				if ci == 1:
					raw_input("[!] Caracter invalido ")
					matrizz[i][j] = 0.0
				else:
					matrizz[i][j] = round(float(aux),5)													
	mostrarmatriz(matrizz,yyy,xxx)

#-------- LIMPIAR MATRIZ ----------

def limpiarmatriz(matrizz,yyy,xxx):
	for i in range (0,int(yyy)):
		for j in range (0,int(xxx)):			
			matrizz[i][j] = 0.0	
	mostrarmatriz(matrizz,yyy,xxx)

#--------------------------------------------GENERALES--------------------------------------------------

def pasarafraccion(numero):
	flag = 0
	flag2 = 0	
	contadordec = 0	
	contadorentero = 0	
	coma = ""
	entero = ""
	exp= 0
	aux=str(round(float(numero),5))
	for i in aux:
		if flag == 0:		
			if i == ".":
				flag = 1
			else:
				contadorentero= contadorentero + 1
				entero = entero + i
		else:
			contadordec = contadordec + 1
			coma = coma + i
	if coma == "":
		return int(numero)	
	if coma == "0":
		return int(entero)
	else:
		exp= 10**contadordec	
		numeroaux= float(numero)*exp		
		while flag2 == 0:		
			flag2 = 1			
			for i in range (2,10):		
				if (numeroaux % i == 0) and (exp % i == 0):
					numeroaux = numeroaux/i
					exp = exp/i
					flag2 = 0
		return (str(int(numeroaux))+"/"+str(exp))

#-------- COMPROBAR MATRIZ ----------

def comprobar(matrizz,yyy,xxx):
	vector = [0,0,0,0,0,0,0]# vector que carga cantidad de 0 por fila.
	mm = 0 # mm es el flag para indicar que esta acomodado.
	while int(mm) == 0:
		vector = [0,0,0,0,0,0,0]
		mm = 1		
		for i in range(0,yyy):# este primer ciclo for carga el vector comentado arriba.
			for j in range(0,xxx):
				if matrizz[i][j] == 0:
					vector[i]=vector[i]+1				
	print vector
	raw_input(":")
#--------------------------------------------LOOP PRINCIPAL--------------------------------------------------

main(yyy,xxx)
	
