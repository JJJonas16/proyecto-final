import json
import logging
import os
from datetime import datetime

from utilidades.decoradores import registrar_operacion

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_DATA = os.path.join(BASE_DIR, "data")
RUTA_HISTORIAL = os.path.join(CARPETA_DATA, "historial.json")

logger = logging.getLogger("calculadora")


def inicializar_historial():
    os.makedirs(CARPETA_DATA, exist_ok=True)
    if not os.path.exists(RUTA_HISTORIAL):
        with open(RUTA_HISTORIAL, "w", encoding="utf-8") as archivo:
            json.dump([], archivo)
        logger.warning("historial creado porque no existía")


def leer_historial():
    try:
        inicializar_historial()
        with open(RUTA_HISTORIAL, "r", encoding="utf-8") as archivo:
            registros = json.load(archivo)
    except (json.JSONDecodeError, UnicodeDecodeError, OSError) as error:
        logger.error("no se pudo leer el historial | %s", error)
        raise
    if not isinstance(registros, list):
        logger.error("el historial no tiene una lista de registros")
        raise ValueError("El archivo del historial no tiene el formato esperado.")
    logger.info("historial leído con %d registros", len(registros))
    return registros


def siguiente_id(registros):
    ultimo = 0
    for registro in registros:
        try:
            numero = int(registro.get("id", "0"))
        except (ValueError, TypeError):
            continue
        if numero > ultimo:
            ultimo = numero
    return str(ultimo + 1).zfill(4)


@registrar_operacion
def guardar_calculo(entradas, resultados):
    registros = leer_historial()
    registro = {
        "id": siguiente_id(registros),
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "entradas": entradas,
        "resultados": resultados,
    }
    registros.append(registro)
    with open(RUTA_HISTORIAL, "w", encoding="utf-8") as archivo:
        json.dump(registros, archivo, ensure_ascii=False, indent=2)
    logger.info("historial escrito | id=%s", registro["id"])
    return registro


def filtrar_historial(registros, fecha=None, material=None):
    filtrados = []
    for registro in registros:
        if fecha is not None:
            if not str(registro.get("fecha", "")).startswith(str(fecha)):
                continue
        if material and material != "Todos":
            if registro.get("entradas", {}).get("material") != material:
                continue
        filtrados.append(registro)
    return filtrados
