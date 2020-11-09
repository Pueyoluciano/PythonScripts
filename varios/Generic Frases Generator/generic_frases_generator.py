import random
import os

class Generic_Generator:
    def __init__(self, tokens=None, nombre="Generic Frases Generator"):
        self.nombre = nombre
        self.tokens = tokens if tokens else ['Token_1', 'Token_2']
        self.conectores = [" " for _ in range(0, len(self.tokens) - 1)]
        
        self.inicializar()
        
    def inicializar(self):
        # Creo una carpeta con el nombre del Generador
        if not os.path.exists(self.nombre):
            os.makedirs(self.nombre)
    
        # Me posiciono en el path
        os.chdir(os.getcwd() + "\\" + self.nombre)
        
        # Creo los token files
        for i, token in enumerate(self.tokens):
            filename = self.token_nombre(i, token)
            
            if not os.path.exists(filename):
                with open(filename, "w") as file:
                    file.write("@completar - Si lees esto es porque tenes que modificar el contenido de los tokens")
    
    def token_nombre(self, i, token):
        return str(i) + "_" + token + ".txt"
    
    def generar(self, repeticiones=1):
        # Levanto los tokens
        tokens_parseados = []
        
        for i, token in enumerate(self.tokens):
            with open(self.token_nombre(i, token), "r") as file:
                lineas = []
                for linea in file.readlines():
                    lineas.append(linea.replace("\n", ""))
                
                tokens_parseados.append(lineas)
            
        # Genero las frases
        salida = []
        
        for _ in range(0, repeticiones):
            generado = ""
            
            for i, token_opciones in enumerate(tokens_parseados):
                generado += random.choice(token_opciones) + (self.conectores[i] if i < len(self.conectores) else "")
            
            salida.append(generado)
            
        return salida
        
if __name__ == "__main__":
    gg = Generic_Generator()
    print(gg.generar(1)[0])