import pygame

def saturar(valor):
    return 255 if valor > 255 else ( 0 if valor < 0 else valor)

class RGB:
    def __init__(self, r=0, g=0, b=0):
        self.r = saturar(r)
        self.g = saturar(g)
        self.b = saturar(b)

    def toList(self):
        return [self.r, self.g, self.b]
        
    def __repr__(self):
        return str([self.r, self.g, self.b])
        
def blender(modo, *colores):
    """
        modo: True  => calcula el promedio de cada componente.
        modo: False => aritmetica saturada.
    """
    
    cant = len(colores)
    res = RGB(0,0,0)
    
    if cant:
        rojo = 0
        verde = 0
        azul = 0
        
        for color in colores:
            rojo += color.r
            verde += color.g
            azul += color.b
            
        if modo:    
            res.r = rojo/cant
            res.g = verde/cant
            res.b = azul/cant
            
        else:
            res.r = saturar(rojo)
            res.g = saturar(verde)
            res.b = saturar(azul)
        
    return res

# -----------------------------------------------
# -----------------------------------------------    

colores = []

colores.append(RGB(127,25,25))
colores.append(RGB(0, 55, 23))
colores.append(RGB(24, 0, 100))

print(colores)

blend = blender(True, *colores)

print(blend)

# -----------------------------------------------

width = 600
height = 400

def drawMain(screen, *colores):
    pygame.draw.rect(screen, blender(True, *colores).toList(), (0, 0, width / 2, height), 0)
    pygame.draw.rect(screen, blender(False, *colores).toList(), (width / 2, 0, width, height), 0)
    
    #Bordes
    pygame.draw.rect(screen, (80,80,80), (0, 0, width / 2, height), 1)
    pygame.draw.rect(screen, (80,80,80), (width / 2, 0, width, height), 1)

def drawBottomLine(screen, *colores):
    x0 = 0
    dx = 0
    y0 = height - (height/4)
    dy = height
    
    salto = width / len(colores)
    
    
    for color in colores:
        dx += salto
        pygame.draw.rect(screen, color.toList(), (x0, y0, dx, dy), 0)
        pygame.draw.rect(screen, (80,80,80), (x0, y0, dx, dy), 1)
        x0 += salto
        
# -----------------------------------------------

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("color Blender")

# -----------------------------------------------

drawMain(screen, *colores)
drawBottomLine(screen, *colores)

pygame.display.flip()

# -----------------------------------------------
running = True
# main loop
while running:
    # event handling, gets all event from the eventqueue
    for event in pygame.event.get():
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            running = False