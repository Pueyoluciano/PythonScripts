import Aplicacion
import Probabilidades as pr
from Menu import *
from Variable import *
from validador import *
#------------------------------------------------
#--------------- TODO ---------------------------
#------------------------------------------------
# 1) Lista de tareas pendientes a implementar.
# 2) Si no te gusta lo sacas :).
#------------------------------------------------
#------------------------------------------------
#------------------------------------------------
class Crypto(Aplicacion.Aplicacion):

    """
    FILLME
    """
    #-----------------------
    #--- inicializacion ----
    #-----------------------
    def iniciar(self,**args):   
        #variables de programa
        self.probs = pr.Probabilidad()
        self.probs.cargarDatos("0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z")
        
        #variables de usuario   
        self.vars["semilla"] = Variable(0,self.modifSemilla,orden=0)
        self.vars["longitudSemilla"] = Variable(16,self.modifLongitudSemilla,orden=1)

        #Items del Menu
        self.agregarMenu(0,Leaf("Encriptar","",self.encriptar))
        self.agregarMenu(1,Leaf("Desencriptar","",self.desencriptar))
        
        self.modifSemilla("semilla")
        
        self.vars["semilla"].valor = self.generarSemilla(self.vars["longitudSemilla"].valor)

    #-----------------------
    #--- Funciones ---------
    #----------------------- 
    def base36encode(self,number, alphabet='0123456789abcdefghijklmnopqrstuvwxyz'):
        """Converts an integer to a base36 string."""
        if not isinstance(number, (int, long)):
            raise TypeError('number must be an integer')

        base36 = ''
        sign = ''

        if number < 0:
            sign = '-'
            number = -number

        if 0 <= number < len(alphabet):
            return sign + alphabet[number]

        while number != 0:
            number, i = divmod(number, len(alphabet))
            base36 = alphabet[i] + base36
        
        return sign + base36
        
    def encriptar(self):
        self.espaciador()
        
        print "Ingrese la clave a encriptar:"
        clave = int(validador.ingresar(str),36)
        
        print "Ingrese la semilla a utilizar:"
        semilla = int(validador.ingresar(str),36)
        
        print "codigo encriptado: (ANOTATELO)"
        print self.doEncriptar(clave,semilla)
        
        self.espaciador()
        
    def doEncriptar(self,clave,semilla):
        return self.base36encode(clave + semilla)
        
    def desencriptar(self):
        self.espaciador()
        print "Ingrese el codigo encriptado:"
        criptado = validador.ingresar(str)
        
        print "Ingrese la semilla utilizada:"
        semilla = validador.ingresar(str)
        
        self.espaciador()
        
        print "el codigo descencriptado es:"
        print self.doDesencriptar(criptado,semilla)
    
    def doDesencriptar(self,criptado,semilla):
        return self.base36encode(int(criptado,36) - int(semilla,36))
    
    def generarSemilla(self,longitud):
        crypto = ""
        for i in range(0,longitud):
            crypto += self.probs.generar()

        return crypto

    #-----------------------
    #--- modificadores -----
    #-----------------------
    # Crear todos los modificadores con esta estructura, y SIEMPRE respetando el encabezado (self,key,*params):     
    def modifSemilla(self,key,*params):
        print "Se genera una nueva Semilla:"
        self.vars["semilla"].valor = self.generarSemilla(self.vars["longitudSemilla"].valor)
        print self.vars["semilla"].valor
    
    def modifLongitudSemilla(self,key,*params):
        print "Ingrese la nueva longitud (entre 5 y 32)"
        longitud = validador.ingresar(int,validador.entre,5,32)
        self.vars["longitudSemilla"].valor = longitud
        self.modifSemilla("semilla")
    
    #-----------------------
    #--- otros -------------    
    #-----------------------    
    # Funcion opcional. Si se desea mostrar algun tipo de informacion ( o ejecutar algun comando)
    # en el menu principal( arriba del nombre de la aplicacion) hay que sobreescribir este metodo.
        
    # Este metodo muestra lo que quieras, la idea es que expliques como se usa el programa.
    def ayuda(self):
        print "Para encriptar: \n"
        print "1) Ingresar la clave que se quiere encriptar."
        print "2) Ingresar una semilla. " + self.appNombre+ " " + self.version + " ofrece una semilla generada de forma aleatoria, de ancho configurable. Su uso es opcional."
        print "3) (RECOMENDABLE) Guardar el codigo encriptado."
        print ""
        print "Para desencriptar:\n"
        print "1) Ingresar el codigo encriptado."
        print "2) Ingresar la semilla utilizada para la encriptacion.\n"
        print "3) Se mostrara en pantalla el codigo desencriptado."
        
    # Texto personalizado de salida.    
    def salirPrint(self):
        pass# self.doEncriptar("Hasta la vista Baby")

#esto siempre va.
# tenes que invocar a tu clase principal, los tres primeros parametros son el nombre, version y si es o no con pantalla grafica.
# despues tenes que pasarle todos los parametros que quieras, separados por comas.
if __name__ == '__main__':
    a = Crypto("Crypto","1.0.0",False)
                    
    a.menuPrincipal()
