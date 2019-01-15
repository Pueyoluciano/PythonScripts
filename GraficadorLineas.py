class linea:
    def __init__(self, desde, hasta, color, sublineas=[]):
        this.desde = desde
        this.hasta = hasta
        this.color = color
        this.sublineas = sublineas

class sublinea(linea):
    def __init__(self, desdePadre, hastaPadre, origen, logntiud, angulo, color):
        # origen = porcentaje respecto del padre (0% es en el origen del padre, 100% es el extremo)
        desde, hasta = calcularDesdeHasta(desdePadre, hastaPadre, origen, longitud, angulo)
        linea.__init__(desde, hasta, color)
        
    def calcularDesdeHasta(self, desdePadre, hastaPadre, origen, longitud, angulo):
        pass
    
    
    
    
    