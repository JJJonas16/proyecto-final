MATERIALES = {
    "Cobre": 1.68e-8,
    "Aluminio": 2.65e-8,
    "Plata": 1.59e-8,
    "Oro": 2.44e-8,
    "Tungsteno": 5.60e-8,
    "Hierro": 9.71e-8,
    "Nicromo": 1.10e-6,
}


def obtener_resistividad(material):
    if material not in MATERIALES:
        raise ValueError("El material seleccionado no es válido.")
    return MATERIALES[material]
