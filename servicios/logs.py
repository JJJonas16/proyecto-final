import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_LOGS = os.path.join(BASE_DIR, "logs")
RUTA_LOG = os.path.join(CARPETA_LOGS, "app.log")


def configurar_logs():
    os.makedirs(CARPETA_LOGS, exist_ok=True)
    logger = logging.getLogger("calculadora")
    logger.setLevel(logging.INFO)
    if logger.handlers:
        return logger

    existia = os.path.exists(RUTA_LOG)
    manejador = logging.FileHandler(RUTA_LOG, encoding="utf-8")
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(module)s.%(funcName)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    manejador.setFormatter(formato)
    logger.addHandler(manejador)

    if not existia:
        logger.warning("archivo de logs creado porque no existía")

    return logger


def leer_logs_recientes(cantidad=50):
    if not os.path.exists(RUTA_LOG):
        return []
    with open(RUTA_LOG, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()
    return lineas[-cantidad:]
