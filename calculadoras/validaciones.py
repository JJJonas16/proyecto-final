import math
import re


class DatoInvalido(Exception):
    pass


# Acepta 2.5, 2,5, 2.5 mm2 y 2,5 mm². Rechaza texto, negativos y mm3.
PATRON_SECCION = r"^\s*(\d+(?:[.,]\d+)?)\s*(?:mm\s*[²2]?)?\s*$"


def convertir_numero(texto, nombre):
    if texto is None:
        raise DatoInvalido("El campo " + nombre + " está vacío.")
    texto = str(texto).strip()
    if texto == "":
        raise DatoInvalido("El campo " + nombre + " está vacío.")
    texto = texto.replace(",", ".")
    try:
        numero = float(texto)
    except ValueError:
        raise DatoInvalido("El campo " + nombre + " debe ser un número.")
    if math.isnan(numero) or math.isinf(numero):
        raise DatoInvalido("El campo " + nombre + " debe ser un número finito.")
    return numero


def validar_positivo(texto, nombre):
    numero = convertir_numero(texto, nombre)
    if numero <= 0:
        raise DatoInvalido("El campo " + nombre + " debe ser mayor que cero.")
    return numero


def validar_seccion(texto):
    if texto is None:
        raise DatoInvalido("La sección transversal está vacía.")
    texto = str(texto).strip()
    if texto == "":
        raise DatoInvalido("La sección transversal está vacía.")
    coincidencia = re.match(PATRON_SECCION, texto)
    if coincidencia is None:
        raise DatoInvalido("La sección transversal no es válida. Use por ejemplo 2.5 o 2,5 mm².")
    numero = float(coincidencia.group(1).replace(",", "."))
    if numero <= 0:
        raise DatoInvalido("La sección transversal debe ser mayor que cero.")
    return numero
