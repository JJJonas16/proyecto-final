# Calculadora de corriente eléctrica

Aplicación web desarrollada con Streamlit para calcular parámetros eléctricos de un cable (resistencia, caída de tensión, resistencia total, potencia disipada y corriente), con registro de historial, logs y exportación de reportes.

## Instalación

1. Activa el entorno virtual `.venv`.
2. Instala las dependencias:
   ```bash
   pip install -r requerimientos.txt

    USO
Ejecuta la aplicación desde la raíz del proyecto:
streamlit run app.py

Estructura principal

app.py: interfaz principal en Streamlit.

calculadora/ y calculadoras/: lógica de cálculos, materiales y validaciones.

servicios/ y utilidades/: historial, logs, reportes y funciones auxiliares.

data/, logs/ y reportes/: datos guardados, registros y archivos exportados.