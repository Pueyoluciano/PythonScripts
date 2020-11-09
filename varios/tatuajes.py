import random

sujeto = ["Perro","Loro","Leñador","Caballero","Pepino","Flor","Oso","Mapache","Escarabajo","Gato","Pitón","Ganzo","Marinero","Robot","Cupido","Pirata","Ballena","Liebre","Cuervo","Tigre","Hamburguesa","Mago","Pollo","Policía","Astronauta","Tiburón","Topo"]

modificador_1 = ["en llamas","congelado","astuto","eterno","viejo","peludo","volador","verde","alegre","llorón","helado","borracho","sorprendido","asustado","enojado","musculoso","canoso","enfurecido","sabio","loco","sucio","mojado","aburrido","risueño","hostil","ruidoso","adormilado","negro","tenebroso","enloquecido","bailarín"]

modificador_2 = ["con un cañon laser","en la luna","disfrazado de goku","en la escoba","en la moto","disfrasado de thanos","en el trono","en botas rojas","tocando el violín","con una botella de ron","disfrazado de mujer maravilla","con un sombrero azul","disfrazado de batman","abrazando a un cactus","en el tractor","disfrazado de superman","en un bote inflable","en la montaña","en el baño","en la playa","con una pata de madera","con tacones","en el avión","con un moretón","con las burbujas","con un hacha","en un tanque"]


while True:
    print(random.choice(sujeto) + " " + random.choice(modificador_1) + " " + random.choice(modificador_2))
    print("")
    if input("Otro ? "):
        break

