import random
from Generales import Generales
import Probabilidades as pr
from Letras import Letras
import Implementador

class Filtros:
    """
    Contiene metodos estaticos, cada uno es un filtro distinto.
    Todos los filtros devuelven aquellas letras que quedan 
    disponibles luego de aplicarse dicho filtro.
    """
    @staticmethod
    def unaConsonante(nombreParcial):
        if(len(nombreParcial) >= 1):
            if(nombreParcial[-1] in Letras.consonantes):
                return Letras.vocales
                
        return Letras.letras

    @staticmethod
    def dosConsonantes(nombreParcial):
        if(len(nombreParcial) >= 2):
            if(nombreParcial[-2] in Letras.consonantes and nombreParcial[-1] in Letras.consonantes):
                return Letras.vocales
                                
        return Letras.letras  
        
    @staticmethod
    def tresConsonantes(nombreParcial):
        if(len(nombreParcial) >= 3):
            if(nombreParcial[-3] in Letras.consonantes and nombreParcial[-2] in Letras.consonantes and nombreParcial[-1] in Letras.consonantes):
                return Letras.vocales
                
            else:
                return Letras.consonantes
                    
        return Letras.letras    
    
    @staticmethod
    def unaVocal(nombreParcial):
        if(len(nombreParcial) >= 1):
            if(nombreParcial[-1] in Letras.vocales):
                return Letras.consonantes
            
        return Letras.letras

    @staticmethod
    def dosVocales(nombreParcial):
        if(len(nombreParcial) >= 2):
            if(nombreParcial[-2] in Letras.vocales and nombreParcial[-1] in Letras.vocales):
                return Letras.consonantes
            
        return Letras.letras  
        
    @staticmethod
    def tresVocales(nombreParcial):
        if(len(nombreParcial) >= 3):
            if(nombreParcial[-3] in Letras.vocales and nombreParcial[-2] in Letras.vocales and nombreParcial[-1] in Letras.vocales):
                return Letras.consonantes
            
        return Letras.letras
            
    @staticmethod
    def soloLetrasAUnaVocal(nombreParcial):
        letrasParcial = Filtros.unaVocal(nombreParcial)
        letrasParcial = letrasParcial.intersection(Filtros.unaConsonante(nombreParcial))
        filtro = Letras.letras.copy()
        filtro.remove("a")
        return letrasParcial.intersection(filtro)
    
    @staticmethod
    def soloLetrasADosVocales(nombreParcial):
        letrasParcial = Filtros.dosVocales(nombreParcial)
        letrasParcial = letrasParcial.intersection(Filtros.unaConsonante(nombreParcial))
        filtro = Letras.letras.copy()
        filtro.remove("a")
        return letrasParcial.intersection(filtro)
    
    @staticmethod   
    def qSiempreConU(nombreParcial):
        if(len(nombreParcial) >= 1):
            if(nombreParcial[-1] == "q"):
                return set(["u"])

        return Letras.letras        
    
    @staticmethod
    def quSiempreConEI(nombreParcial):
        if(len(nombreParcial) >= 2):
            if(nombreParcial[-2]+nombreParcial[-1] == "qu"):
                return set(["e","i"])

        return Letras.letras


class ListadoReglas:
    """
    -Contenedor de todos los filtros(reglas) implementados.
    la variable contenido es una instancia de Implementaciones.
    """
    contenido = Implementador.Implementaciones()
    
    contenido.agregarItem("unaVocal","Permite solo una vocal entre consonantes",Filtros.unaVocal)
    contenido.agregarItem("dosVocales","Permite hasta dos vocales juntas",Filtros.dosVocales)
    contenido.agregarItem("tresVocales","Permite hasta tres vocales juntas",Filtros.tresVocales)
    contenido.agregarItem("unaConsonante","Permite solo una consonante entre vocales",Filtros.unaConsonante)
    contenido.agregarItem("dosConsonantes","Permite hasta dos consonantes juntas",Filtros.dosConsonantes)
    contenido.agregarItem("tresConsonantes","Permite hasta tres consonantes juntas",Filtros.tresConsonantes)
    contenido.agregarItem("qSiempreConU","Siempre que aparece una Q la sigue una U",Filtros.qSiempreConU)
    contenido.agregarItem("quSiempreConEI","Si aparece QU le sigue una E o una I",Filtros.quSiempreConEI)   
    contenido.agregarItem("soloLetrasAUnaVocal","unaConsonanteUnaVocal + vocales unicamente A",Filtros.soloLetrasAUnaVocal)
    contenido.agregarItem("soloLetrasADosVocales","unaConsonanteHastaDosVocales + vocales unicamente A",Filtros.soloLetrasADosVocales)

    
class MotorReglas:

    """
    - Administra un listado de reglas, guardando en self.reglas aquellas que estan activas.
    
    - Permite obtener una letra filtrando previamente aquellas que no cumplan las reglas cargadas.
    
    - Para obtener las letras se usa el modulo Probabilidades.py, que permite ponderar la probabilidad
      de aparicion de cada letra.
      
    - self.reglas es una lista de strings, con los nombres de los Filtros (reglas) cargados en ListadoReglas.
      Ej: self.reglas = ["tresVocales","dosConsonantes","qSiempreConU","quSiempreConEI"]
    
    
    - Metodos:
    
    - reglasActivas(self, *reglasTemporal)
        Devuelve una lista con todas las reglas, indicando aquellas que estan activas.
        Utilizado para visualizar dicha info, tiene este formato:
        ["[ ] nombreReglaNoActiva1",
         "[x] nombreReglaSiActiva2",
         "[x] nombreReglaSiActiva3",
         "[ ] nombreReglaNoActiva4",
         "]
        Si reglasTemporal esta vacio, valido contra las reglas en self.reglas.
        Si no es asi, valido contra la lista que me llega por parametro. 
    
    - agregarReglas(self,params)
        espera recibir en params una lista con reglas.
        realiza un append a la lista de reglas.
    
    - limpiarReglas(self)
        pone en cero la lista de reglas: self.reglas = []
        
    - nuevaLetra(self,nombreParcial)
        Se aplican todos los filtros seteados, y de las letras resultantes
        se obtiene una letra de manera aleatoria respetando la distribucion
        de probabilidades asignada.
        Si los filtros no dejan letras disponibles se termina el proceso con una
        excepcion.
    """
    
    def __init__(self):
        self.reglas = []
        
        self.probAuxiliar = pr.Probabilidad() # Distribucion de probs auxiliar. 
        self.probabilidades = pr.Probabilidad() #Distribucion de probs que se usa como referencia (este se cambia bajo demanda del usuario).
        abcdario = list(Letras.letras)
        abcdario.sort()
        self.probabilidades.cargarDatos(abcdario)
    
    def reglasActivas(self, *reglasTemporal):
        listadoCompleto = [item.nombre for item in ListadoReglas.contenido.contenido]
        
        if(len(reglasTemporal) == 0):
            reglasAComparar = [item.nombre for item in self.reglas]
              
        else:
            reglasAComparar = reglasTemporal[0]
            
        return ["[x] " + regla if regla in reglasAComparar else "[ ] " + regla for regla in listadoCompleto]
        
    def agregarReglas(self,params):
        for regla in params:
            self.reglas.append(regla)

    def limpiarReglas(self):
        self.reglas = []
            
    def nuevaLetra(self,nombreParcial):
        letrasPosibles = Letras.letras
        for regla in self.reglas:
            letrasPosibles = letrasPosibles.intersection(regla.accionParametro(nombreParcial))
        
        if(len(letrasPosibles) == 0):
            raise Exception("Las reglas filtran todas las letras :(")
        
        # Esta operacion filtra la lista completa(todas las letras) quedandose con aquellas que
        # esten en letrasPosibles.
        probs = filter(lambda x: x[0] in letrasPosibles, self.probabilidades.listarProbabilidades())
        
        # Ahora calculo la probabilidad que resulta de los elementos filtrados ( siempre es <= 1)
        # y la reparto equitativamente entre estos para obtener probabilidad total = 1.
        probParcial = (1.0 - reduce(lambda x,y: x+y, [elemento[1] for elemento in probs])) / (len(probs))
        probs = map(lambda x: [x[0], x[1] + probParcial], probs)

        # actualizo mi probabilidades auxiliar, para que tenga los datos recien calculados.
        self.probAuxiliar.cargarTodo(probs)
        
        return self.probAuxiliar.generar()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
