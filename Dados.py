from Probabilidades import Probabilidad
from validador import *

a = Probabilidad()
a.cargarDatos("1","2","3","4","5","6")
uno    = [" ------- ","|       |","|   #   |","|       |"," ------- "]
dos    = [" ------- ","| #     |","|       |","|     # |"," ------- "]
tres   = [" ------- ","| #     |","|   #   |","|     # |"," ------- "]
cuatro = [" ------- ","| #   # |","|       |","| #   # |"," ------- "]
cinco  = [" ------- ","| #   # |","|   #   |","| #   # |"," ------- "]
seis   = [" ------- ","| #   # |","| #   # |","| #   # |"," ------- "]
diccio = {"1":uno,"2":dos,"3":tres,"4":cuatro,"5":cinco,"6":seis}

def dado(*repeticiones):
    tiradas = 1
    if (len(repeticiones) > 0):
        tiradas = repeticiones[0]
    
    else:
        tiradas = 1
        
    for i in range(0,tiradas):
        numero = a.generar()
        resultado = diccio[numero]
        for fila in resultado:
            print fila
            
seguir = True
while (seguir):            
    print "indique la cantidad de tiradas:"
    ingreso = validador.ingresar(int,validador.entre,0,20)
    if(ingreso == 0):
        print "KeepRollingDice4Life"
        seguir = False
    else:
        dado(ingreso)
    # print "otro?"
    # seguir = validador.ingresarSINO()