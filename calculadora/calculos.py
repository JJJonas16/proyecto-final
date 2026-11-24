from calculadora.materiales import obtener_resistividad
from utilidades.decoradores import registrar_operacion


def convertir_area(area_mm2):
    return area_mm2 * 10 ** -6


def longitud_total(longitud_ida):
    return 2 * longitud_ida


def resistencia_cable(resistividad, longitud, area_m2):
    return resistividad * longitud / area_m2


def resistencia_total(resistencia_carga, rc):
    return resistencia_carga + rc


def corriente(tension, rt):
    return tension / rt


def caida_tension(i, rc):
    return i * rc


def potencia_disipada(i, rc):
    return i ** 2 * rc


@registrar_operacion
def calcular_todo(entradas):
    resistividad = obtener_resistividad(entradas["material"])
    area = convertir_area(entradas["seccion"])
    longitud = longitud_total(entradas["longitud_ida"])
    rc = resistencia_cable(resistividad, longitud, area)
    rt = resistencia_total(entradas["resistencia_carga"], rc)
    i = corriente(entradas["tension"], rt)
    vc = caida_tension(i, rc)
    pc = potencia_disipada(i, rc)
    return {
        "rc": rc,
        "rt": rt,
        "corriente": i,
        "caida_tension": vc,
        "potencia": pc,
    }
