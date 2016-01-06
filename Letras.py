class Letras:

    """
    - Contenedor de letras (no incluye la enie).
    - Tiene tres set():
        - vocales.
        - consonantes.
        - letras.
    - Tener en cuenta que al ser Set(), no tienen orden,
      por lo que de ser necesario, se deben castear a list()
      y ordenar el nuevo objeto con el metodo conveniente.
    """
    
    vocales = set(["a","e","i","o","u"])
    consonantes = set(["b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","y","z"])
    letras = vocales.union(consonantes)
