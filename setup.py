from distutils.core import setup  
import sys
import getopt
import py2exe

try:
	scriptName = sys.argv[3]
except NameError:
	print "Usage: python setup.py py2exe -i NombreDelScript " # el nombre del archivo va sin extension!!
 	sys.exit(2)
	
# Para crear el exe hay que ir al cmd y correr python setup.py py2exe
setup(name=scriptName, 
 version="2.0", 
 description="yatusabe", 
 author="Pueyo Luciano", 
 author_email="PueyoLuciano.getMail()", 
 url="http://cafeidotica.blogspot.com.ar/", 
 license="Mozilla Public License 2.0", 
 scripts=[scriptName + ".py",], 
 console=[scriptName + ".py"], 
 options={"py2exe": {"bundle_files": 1}}, 
 zipfile=None,
)
