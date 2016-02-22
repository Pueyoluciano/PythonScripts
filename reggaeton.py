import os
from validador import *
import random

sujeto = ["Mami","Gata","Perra","Zorra","Chica"]
yo = ["yo quiero","vamos a","yo voy a","yo extrano","yo vengo a"]
accion = ["castigarte","encenderte","darte","azotarte","tocarte"]
adjetivo = ["duro","rapido","lento","suave","fuerte"]
tiempo = ["hasta que salga el sol","toda la noche","hasta el amanecer","hasta manana","todo el dia"]
adjetivo2 = ["sin miedo","sin anestesia","en el piso","contra la pared","sin compromiso"]

cancion = [sujeto,yo,accion,adjetivo,tiempo,adjetivo2]

seguir = True

while(seguir):
    frase = ""
    
    for parte in cancion:
        frase += random.choice(parte) + " "

    print frase	
    print "otro reggeton?"
    seguir = validador.ingresarSINO()