#-------------------------------------------------
# ------------------  IMPORTS  -------------------
#-------------------------------------------------
import matematica

#-------------------------------------------------
# ------------------  ACCIONES  ------------------
#-------------------------------------------------
print "division entera"
print "dividendo:"
a = matematica.convertir('int')
print "divisor:"
b = matematica.convertir('int')
resultado,resto = matematica.divent(a,b)

print str(a)+"/"+str(b)+ " = " + str(resultado)
print "resto: " + str(resto)



