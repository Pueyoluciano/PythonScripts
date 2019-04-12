# import pygame
import threading
import drumExMachina

class _DXFConsola:
    
    salir_codes = [0, "0", "salir", "exit"]
    
    def __init__(self):
        pass

    def loop(self):
        salir = False
        
        while not salir:
            user_input = input("> ")
            salir = user_input in self.salir_codes
                
    
class _DXFGrafico:
    def __init__(self, ancho=1200, alto=800):
        self.alto = alto
        self.ancho = ancho
        
        self.screen = pygame.display.set_mode([self.ancho, self.alto])
        pygame.display.set_caption("Drum Ex Machina")

    def loop(self):
        self.engine.loop()
        
        pygame.init()
        
        clock = pygame.time.Clock()
        
        salir = False
        while not salir:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    salir = True
                    
            pygame.draw.rect(self.screen, [255,0,0], [75, 10, 50, 20] , 1)
                    
                    
            pygame.display.flip()
            pygame.time.delay(50)
        
        
class DrumExFacade:
    """
        Interfaz de DrumExMachina.
        
        Tiene dos modos de uso, consola y grafico.
    """
    
    def __init__(self, modo='consola', ancho=1200, alto=800):
        self.modo = modo
        self.engine = None
        
        # Modo: Consola | grafico
        self.engine = _DXFConsola() if modo == 'consola' else _DXFGrafico(alto, ancho)
            
    def loop(self):
        DXM_thread = threading.Thread(target=drumExMachina.testeos)
        DXM_thread.start()
        
        self.engine.loop()
        
        DXF_thread.exit()
        DXM_thread.exit()
            
DXF = DrumExFacade("consola")


DXF_thread = threading.Thread(target=DXF.loop)

DXF_thread.start()            