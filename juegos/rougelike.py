import sys
import time
import pygame

clock = pygame.time.Clock()

class Accion:
    def __init__(self, nombre, turnos):
        self.nombre = nombre
        self.turnos = turnos

    def ejecutar(self):
        return self.nombre
   
    def avanzar(self):
        self.turnos -= 1
   
    def estaLista(self):
        return self.turnos == 0
   
class Actor:
    def __init__(self, nombre, raza, clase):
        # Identidad
        self.nombre = nombre
        self.raza = raza
        self.clase = clase
        self.nivel = 1
        self.experiencia = 0
        
        # Signos vitales
        self.vida = [10,10]
        self.mana = [5,5]
        self.energia = [10,10]

        self.atributos = {
            'fuerza': 10,
            'inteligencia': 5,
            'constitucion': 10,
            'agilidad': 10,
            'suerte': 50,
        }
        
        # ---
        self.accion = None
        
    def decidir(self, accion, turnos):
        self.accion = Accion(accion, turnos)
        
    def actuar(self):
        print(self.nombre + "-> " + self.accion.ejecutar())
        self.accion = None
        
        
class Interfaz:
    def __init__(self, alto, ancho, titulo):
        self.alto = alto
        self.ancho = ancho
        self.titulo = titulo
        pygame.init()
        
        self.screen = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption(titulo)

class DungeonMaster:
    def __init__(self):
        self.tiempo = 0
        self.actores = []
        
        self.actores.append(Actor("John Salchicha", "Humano", "Paladin"))
        self.actores.append(Actor("Damian Salaman", "Orco", "Guerrero"))
    
    def _inicializacion(self):
        self.interfaz = Interfaz(400, 400, "EL ROGUELIKE")
        
        
    
    def loop(self):
        #Inicializaciones
        self._inicializacion()
        
        findeljuego = False
        
        while not findeljuego:
            # Se renderiza todo
            changed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

            pygame.display.update()
            clock.tick(60) # limit to 60 fps
            
            self.tiempo += 1
            print("Turno: ", self.tiempo)
    
            # Actores eligen accion (si están sin accion)
            for actor in self.actores:
                if not actor.accion:
                    if actor.nombre == "John Salchicha":
                        actor.decidir("Accion_1", 5)
                        
                    else:
                        actor.decidir("Accion_2", 3)
            
            # Avanza un turno y se ejecutan las acciones listas
            for actor in self.actores:
                actor.accion.avanzar()
                
                if actor.accion.estaLista():
                    actor.actuar()
            
            
            # time.sleep(1)
            
DM = DungeonMaster()

DM.loop()