import csv
import logging
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_REPORTES = os.path.join(BASE_DIR, "reportes")

logger = logging.getLogger("calculadora")

COLUMNAS = [
    "id",
    "fecha",
    "tension_v",
    "resistencia_carga_ohm",
    "material",
    "longitud_ida_m",
    "seccion_mm2",
    "rc_ohm",
    "rt_ohm",
    "corriente_a",
    "caida_v",
    "potencia_w",
]


def exportar_csv(registros):
    if not registros:
        raise ValueError("No hay registros para exportar.")

    os.makedirs(CARPETA_REPORTES, exist_ok=True)
    nombre = "reporte_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"
    ruta = os.path.join(CARPETA_REPORTES, nombre)

    try:
        with open(ruta, "w", encoding="utf-8-sig", newline="") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(COLUMNAS)
            for registro in registros:
                entradas = registro.get("entradas", {})
                resultados = registro.get("resultados", {})
                escritor.writerow([
                    registro.get("id", ""),
                    registro.get("fecha", ""),
                    entradas.get("tension", ""),
                    entradas.get("resistencia_carga", ""),
                    entradas.get("material", ""),
                    entradas.get("longitud_ida", ""),
                    entradas.get("seccion", ""),
                    f"{resultados.get('rc', 0):.4f}",
                    f"{resultados.get('rt', 0):.4f}",
                    f"{resultados.get('corriente', 0):.4f}",
                    f"{resultados.get('caida_tension', 0):.4f}",
                    f"{resultados.get('potencia', 0):.4f}",
                ])
    except OSError as error:
        logger.error("no se pudo escribir el reporte | %s", error)
        raise

    logger.info("reporte exportado | archivo=%s", nombre)
    return ruta
