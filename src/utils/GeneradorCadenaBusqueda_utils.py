import itertools

def generar_cadenas_busqueda(terminos_pico, min_terminos=4, max_terminos=5):
    cadenas_busqueda = []

    # Generar combinaciones de términos únicos
    for i in range(min_terminos, max_terminos + 1):
        combinaciones = [(c, sum(peso for termino, peso in c)) for c in itertools.combinations(terminos_pico, i) if len(set(c)) == i]
        for combinacion, peso_total in combinaciones:
            cadena = " AND ".join(termino for termino, _ in combinacion)
            cadenas_busqueda.append((cadena, peso_total))

    # Ordenar las cadenas de búsqueda por relevancia (peso total)
    cadenas_busqueda.sort(key=lambda x: x[1], reverse=True)

    # Obtener solo las cadenas de búsqueda sin los pesos
    cadenas_busqueda = [cadena for cadena, _ in cadenas_busqueda]

    return cadenas_busqueda