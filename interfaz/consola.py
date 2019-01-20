class Menu:
    def __init__(self, nodoRaiz):
        self.nodoRaiz = nodoRaiz
        self.nodoRaiz.SoyRaiz = True

        
class Nodo:
    def __init__(self, nombre, texto, accion, *submenus):
        self.nombre = nombre
        self.texto = texto
        self.submenus = submenus
        self.soyRaiz = False
        
    def soyHoja(self):
        return False if self.submenus else True
        
        
if __name__ == "__main__":
    pass