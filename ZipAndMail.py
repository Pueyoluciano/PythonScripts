import os
import sys
import zipfile
from Generales import Generales

# print sys.argv

def createZip(zipName="PythonsScripts.zip"):
    os.chdir("C:\\Python27")
    archivos = [archivo for archivo in os.listdir(".") if os.path.splitext(archivo)[1] in[".py",".txt"]]
    print "-----------------------------"
    print "archivos encontrados:"
    print "-----------------------------"
    
    Generales.enumerarLista(archivos)

    zipeado = zipfile.ZipFile(zipName, "w")
    for archivo in archivos:
        zipeado.write(archivo)
        
    print "-----------------------------"
    print zipName + " creado"    
    print "-----------------------------"
    zipeado.close()
    raw_input("Presione una tecla para continuar...")

if (len(sys.argv) > 1):
    createZip(sys.argv[1])
else:
    createZip()