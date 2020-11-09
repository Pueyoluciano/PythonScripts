from generic_frases_generator import Generic_Generator as GG

if __name__ == "__main__":
    rg = GG(['sujeto', 'yo', 'accion', 'adjetivo', 'tiempo', 'adjetivo2'], 'Reggateon Generator')
    
    print(rg.generar(1)[0])