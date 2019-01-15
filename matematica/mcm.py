#-------------------------------------------------
#-------------------  Imports  -------------------
#-------------------------------------------------
import os
import matematica

#-------------------------------------------------
#-----------------  acciones  --------------------
#-------------------------------------------------
os.system("clear")
print "Minimo Comun Multiplo entre:"
a = matematica.convertir("int")
b = matematica.convertir("int")
print "= " + str(matematica.mcm(a,b))
