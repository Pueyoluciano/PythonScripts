import random
from validador import *
seguir = True
while (seguir):
    a = range(0,46)
    b = []
    c = -1
    for i in range(0,6):
        c = random.choice(a)
        b.append(c)
        a.remove(c)
    
    print "--------------------"
    print b
    seguir = validador.ingresarSINO()