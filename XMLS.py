class Tag:
    def __init__(nombre,atributos,valor):
        self.nombre = nombre
        self.atributos = atributos
        self.valor = valor

        
    arch = open("C:\\Python27\\xmlTest.xml", "r")
    file = arch.read()        

def obtenerAtributos(tag):
    atributos = {}
    #separo los atributos nombre="valor"
    attrs = tag.split(" ")[1:]
    
    for attr in attrs:
        nombre, valor = attr.split("=")
        atributos[nombre] = valor
    
    return atributos
    
def resolverXML(file, pos):

    entreEnTag = False
    buscoContenido = False
    contenido = ""
    nombreTag  = ""
    tagActual = ""
    
    for letra in file[pos:]:
        if(letra == "<"):
            tagActual += letra
            entreEnTag = True
            nombreTag = ""
            pos += 1
            
        else:
            if(entreEnTag):
                if(letra == ">"):
                    tagActual += letra
                    # entreEnTag = False
                    buscoContenido = True
                    pos += 1
                    print nombreTag
                    
                    #Aca Termine de encontar un tag
                    
                    if(file[pos] == "<"):
                        nodo = Tag(nombreTag, obtenerAtributos(nombreTag),resolverXML(file,pos))
                        
                    else:
                        estoyEnLeaf = True
                    
                else:
                    nombreTag += letra
                    pos += 1
                    
            else:
                if(estoyEnLeaf):
                    if(letra == "<"):
                       return Tag(nombreTag, obtenerAtributos(nombreTag), contenido)
                    else:
                        contenido += letra
                        pos += 1
                        estoyEnLeaf = False
# <root>
    # <tag1 atributo1="pedro">asd</tag1>
    # <tag2>
        # <tag4>asd32</tag4>
    # </tag2>
    # <tag5/>
# </root>    
            

            # if(buscoContenido):
                # if(letra == "<"):
                    # tagSiguiente += letra
                    # entreEnTagSiguiente = True
                    # nombreTagSiguiente = ""
                    # pos += 1
                    
                # else:
                    # if(entreEnTagSiguiente):
                        # if(letra == ">"):
                            # tagSiguiente += letra
                            # entreEnTagSiguiente = False
                            # pos += 1
                            # print nombreTag
                            
                        
                # contenido += letra

             
# Un Tag es una 3-upla:
# [nombre, atributos, valor]
# donde atributos es un diccionario con los atributos cargados
# donde valor es una lista de Tags, o un valor concreto.
#[]
                    
["root",{},
    [["tag1",{"atributo1":"pedro"},"asd"],
     ["tag2",{},
        [["tag4",{},"asd32"]]
     ],
     ["tag5",{""},""]
    ]
]
    