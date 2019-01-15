import os
import random

sujeto = ["Mami","Gata","Perra","Zorra","Chica"]
yo = ["yo quiero","vamos a","yo voy a","yo extrano","yo vengo a"]
accion = ["castigarte","encenderte","darte","azotarte","tocarte"]
adjetivo = ["duro","rapido","lento","suave","fuerte"]
tiempo = ["hasta que salga el sol","toda la noche","hasta el amanecer","hasta manana","todo el dia"]
adjetivo2 = ["sin miedo","sin anestesia","en el piso","contra la pared","sin compromiso"]

dic = [sujeto,yo,accion,adjetivo,tiempo,adjetivo2]
frase = ""

os.system('clear')

for i in range(0,5):
	a = int(round(4*random.random()))
	frase +=" " + dic[i][a]

print frase	

