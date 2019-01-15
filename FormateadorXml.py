    
#<root><tag1>asd</tag1><tag2><tag4>asd32</tag4></tag2><tag5/></root>

def xmlDeclarationTagMethod():
    pass
    
def openingNodeTagMethod():
    pass
    
def closingNodeTagMethod():
    pass
    
def openingLeafTagMethod():
    pass
    
def closingLeafTagMethod():
    pass
    
def emptyTagMethod():
    pass

tab = "    "
    
methods = {"xmlDeclarationTagMethod": xmlDeclarationTagMethod,
            "openingNodeTagMethod": openingNodeTagMethod, 
            "closingNodeTagMethod": closingNodeTagMethod, 
            "openingLeafTagMethod": openingLeafTagMethod, 
            "closingLeafTagMethod": closingLeafTagMethod, 
            "emptyTagMethod":emptyTagMethod}


def formatXml():
    seguir = True
    while(seguir):
        tag = findNextTag()
        if(tag == ""):
            seguir = False
            
        else:    
            tagTypeMethod = identityTagType()
            methods[tagTypeMethod]()

            
#<root><tag1>asd</tag1><tag2><tag4>asd32</tag4></tag2><tag5/></root>
            
    if("<?" in tag):
       return "xmlDeclarationTag"
       
    if("/" not in tag):
        if(getTagName(tag) == getTagName(nextTag)):
        #openingLeafTab
            return "openingLeafTag"
        else:
        #openingNodeTab
            return "openingNodeTag"
        
    else:
        return "closingTag"
        
        
        
    if(nextTag[1] == "/"):
    
        return 
       
def formatXML():
    pos = 0
    
    tag,pos = getNextTag(pos)
    nextTag,pos = getNextTag(pos)
    
    if("<?" in tag):
        # xmlDeclarationTag
        pass
        
    else:
        if("/" not in tag):
            if(getTagName(tag) == getTagName(nextTag)):
            #openingLeafTab
            
            else:
            #openingNodeTab
            
        else:


def getTagName(tag):
    retorno = ""
    for letra in tag:
        if letra not in ["/","\\","","<",">","?"]:
            if letra != " ":
                retorno += letra
            
            else:
                break
                
    return retorno
    
def getNextTag(file,pos):
    tag = ""
    seguir = True
    inicioDeTag = False
    
    while(seguir):
        letra = file.read(1)
        if (letra == ''):
            print "EOF"
            return "EOF", pos
        
        if(letra == "<"):
           tag += letra
           pos += 1
           inicioDeTag = True
           
        else:
            if(inicioDeTag):
                if(letra == ">"):
                    tag += letra
                    pos += 1
                    seguir = False
                    
                else:
                    tag += letra
                    pos += 1
    return tag, pos
            

def FormateadorXML(ruta):
    file = open(ruta, "r+")
    pos = 0
    tagAndPos = ""
    while(tagAndPos!= "EOF"):
        tagAndPos = getNextTag(file,pos)
        print tagAndPos[0]
    
    # tagAndPos = getNextTag(file,pos)
    # print tagAndPos[0]

    
    # tagAndPos = getNextTag(file,pos)
    # tag = tagAndPos[0]
    # nextTag = getNextTag(file,tagAndPos[1])
    
    # print getTagType(tag,nextTag[0])
    # print getTagName(tagAndPos[0])
    # print tagAndPos[0]
    # print "-------------------------------------------------------------"
    # tagAndPos = getNextTag(file,nextTag[1])
    # tag = tagAndPos[0]
    # nextTag = getNextTag(file,tagAndPos[1])
    
    # print getTagType(tag,nextTag[0])
    # print getTagName(tagAndPos[0])
    # print tagAndPos[0]
    # print "-------------------------------------------------------------"
    # tagAndPos = getNextTag(file,nextTag[1])
    # tag = tagAndPos[0]
    # nextTag = getNextTag(file,tagAndPos[1])
    
    # print getTagType(tag,nextTag[0])
    # print getTagName(tagAndPos[0])
    # print tagAndPos[0]
    
    
    file.close()


FormateadorXML("C:\\Python27\\xmlTest.xml")

    
# openingNodeTag <root>
# closingNodeTag </root>
# openingLeafTag <tag1>contenido
# closingLeafTag </tag1>
# emptyTag       <tag2/>


# openingNodeTag:
    # me paro al final del tag
    # borro contenido entre tags
    # enter y sumo un tab

# closingNodeTag:
    # me paro al principio del tag
    # resto un tab
    # borro contenido entre tags
    # enter
    
# openingLeafTag & closingLeafTag:
    # me paro al final del closingLeafTag
    # enter
    
# emptyTag:
    # me paro al final del tag
    # enter
    
    



