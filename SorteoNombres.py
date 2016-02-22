import os
import Probabilidades as pr
from Generales import Generales

a = pr.Probabilidad()
archivo = "ListaNombres.txt"

if(os.path.isfile(archivo)):
    file = open("ListaNombres.txt","r")
    
else:
    file = open("ListaNombres.txt","w")
    file.write("Nombre1\n")
    file.write("Nombre2\n")
    file.write("Nombre3")
    file.close()
    file = open("ListaNombres.txt","r")

a.cargarDatos(map(lambda x: x[0:-1] if "\n" in x else x, filter(lambda x: True if x[0] != "#" else False, file.readlines())))

print "Concursantes:"
Generales.enumerarLista(a.listarItems())

print "El ganador es:\n"
raw_input("...")
print "\n" + a.generar() + "\n"
raw_input("...")

file.close()