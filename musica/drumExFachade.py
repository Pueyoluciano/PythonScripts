import pygame

class DrumExFacade:
    
    def __init__(self, ancho, alto):
        self.alto = alto
        self.ancho = ancho
        self.screen = pygame.display.set_mode((ancho,alto))
        pygame.display.set_caption("Drum Ex Machina")
        
        
    def loop(self):
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
            
            
DXF = DrumExFacade(1200, 800)
DXF.loop()

            