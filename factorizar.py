#-------------------------------------------------
# ------------------  IMPORTS  -------------------
#-------------------------------------------------
import math
import time
import matematica

#-------------------------------------------------
# ------------------  ACCIONES  ------------------
#-------------------------------------------------
a = matematica.convertir('long')
resultado,tiempo = matematica.factorizar(a,1)
print resultado
print "Calculado en: " + str(tiempo)
raw_input("Grosso...")
#j = 2
#for i in range(0,100):
#	j = iterar(j)
#	print j

#asd = factorizar(long(exp(2,127))-1)
#print asd

#algunos primos
# 982451653
# 200364773467423
# 36413321723440003717 20 cifras. 
# 671998030559713968361666935769 30 cifras.
# 170141183460469231731687303715884105727
# 2425967623052370772757633156976982469681 

def asd(numero):
	jj = 0
	tiempo = time.time()
	for i in range(0,numero):
		jj = matematica.iterar(jj)
		print jj
	tiempototal = (time.time()-tiempo) 
	print tiempototal

#asd(40)






