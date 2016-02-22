from distutils.core import setup  
import sys
import py2exe

try:
    scriptName = sys.argv[3]

except IndexError:
    print "Usage: python setup.py py2exe -i nombreApp"
    sys.exit(2)
    
# Para crear el exe hay que ir al cmd y correr python setup.py py2exe
setup(
 name=scriptName, 
 version="2.0", 
 description="Aplicacion Python creada con py2exe", 
 author="Pueyo Luciano", 
 author_email="PueyoLuciano.getMail()", 
 url="http://cafeidotica.blogspot.com.ar/", 
 license="Mozilla Public License 2.0", 
 scripts=[scriptName + ".py"], 
 console=[{"script":scriptName + ".py", "icon_resources": [(1, "pyc.ico")]}], 
 options={"py2exe": {"bundle_files": 1}}, 
 zipfile=None,
 # windows=[{"script":scriptName + ".py" , "icon_resources": [(1, "pyc.ico")] }] <<-- si configuras el windows, corre el .exe como un proceso.
)     