import logging
import time

logger = logging.getLogger("calculadora")


def registrar_operacion(funcion):
    def envoltura(*args, **kwargs):
        inicio = time.perf_counter()
        try:
            resultado = funcion(*args, **kwargs)
        except Exception as error:
            duracion = time.perf_counter() - inicio
            logger.error("%s falló después de %.4f s | %s", funcion.__name__, duracion, error)
            raise
        duracion = time.perf_counter() - inicio
        logger.info("%s completado en %.4f s", funcion.__name__, duracion)
        return resultado

    envoltura.__name__ = funcion.__name__
    return envoltura
