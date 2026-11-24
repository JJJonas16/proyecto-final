def iterar_historial(registros):
    for registro in registros:
        yield registro


def iterar_logs(lineas):
    for linea in lineas:
        texto = linea.strip()
        if texto:
            yield texto
