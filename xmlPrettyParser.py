import xml.dom.minidom
from datetime import datetime
import os
import sys

print "indicar la ruta completa del xml a pretty parsear."
ruta = raw_input("> ")
try:
    xml = xml.dom.minidom.parse(ruta) # or xml.dom.minidom.parseString(xml_string)
        
    file = open("xmlOut.xml","w")

    pretty_xml_as_string = xml.toprettyxml()

    file.write(pretty_xml_as_string.encode('utf8', 'replace'))

    print "--------------------------------------------------------"
    print "Archivo generado: xmlOut.xml"
    print "--------------------------------------------------------"

    file.close()

    os.startfile("xmlOut.xml")
    
except Exception as exc:
    log = open("xmlParserLog.txt", "a")
    log.write(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + " -- " + str(exc) + "\n")
    print str(exc)
    log.close()