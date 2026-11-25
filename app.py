import os

import streamlit as st

from calculadora import calculos
from calculadora.materiales import MATERIALES
from calculadoras.validaciones import DatoInvalido, validar_positivo, validar_seccion
from servicios import historial, logs, reportes
from utilidades.generadores import iterar_historial, iterar_logs

st.set_page_config(
    page_title="Calculadora de corriente eléctrica",
    page_icon="⚡",
    layout="wide",
)

logger = logs.configurar_logs()


def iniciar_aplicacion():
    if "iniciada" not in st.session_state:
        logger.info("aplicación iniciada")
        st.session_state["iniciada"] = True


iniciar_aplicacion()

if "resultado" not in st.session_state:
    st.session_state["resultado"] = None


def limpiar_formulario():
    st.session_state["tension"] = ""
    st.session_state["resistencia"] = ""
    st.session_state["longitud"] = ""
    st.session_state["seccion"] = ""
    st.session_state["resultado"] = None


def pagina_calculadora():
    st.title("Calculadora de corriente eléctrica")
    st.write("Circuito DC en serie con cable de ida, carga y cable de retorno.")

    with st.form("formulario_calculo"):
        tension = st.text_input("Tensión de la fuente (V)", key="tension", placeholder="Ejemplo: 12")
        resistencia = st.text_input("Resistencia de la carga (Ω)", key="resistencia", placeholder="Ejemplo: 10")
        material = st.selectbox("Material del conductor", list(MATERIALES.keys()), key="material")
        longitud = st.text_input("Longitud de ida (m)", key="longitud", placeholder="Ejemplo: 5")
        seccion = st.text_input("Sección transversal (mm²)", key="seccion", placeholder="Ejemplo: 2,5")
        calcular = st.form_submit_button("Calcular")

    st.button("Limpiar formulario", on_click=limpiar_formulario)

    if calcular:
        try:
            entradas = {
                "tension": validar_positivo(tension, "Tensión"),
                "resistencia_carga": validar_positivo(resistencia, "Resistencia de carga"),
                "material": material,
                "longitud_ida": validar_positivo(longitud, "Longitud de ida"),
                "seccion": validar_seccion(seccion),
            }
            resultados = calculos.calcular_todo(entradas)
            historial.guardar_calculo(entradas, resultados)
            st.session_state["resultado"] = resultados
            st.success("Cálculo realizado y guardado en el historial.")
        except DatoInvalido as error:
            logger.warning("validación rechazada | %s", error)
            st.session_state["resultado"] = None
            st.error(str(error))
        except Exception as error:
            logger.error("no se pudo completar el cálculo | %s", error)
            st.session_state["resultado"] = None
            st.error("No se pudo completar el cálculo: " + str(error))

    resultado = st.session_state["resultado"]
    if resultado is not None:
        st.subheader("Resultados")
        col1, col2, col3 = st.columns(3)
        col1.metric("Resistencia del cable (Rc)", f"{resultado['rc']:.4f} Ω")
        col2.metric("Resistencia total (Rt)", f"{resultado['rt']:.4f} Ω")
        col3.metric("Corriente (I)", f"{resultado['corriente']:.4f} A")
        col4, col5, _ = st.columns(3)
        col4.metric("Caída de tensión (Vc)", f"{resultado['caida_tension']:.4f} V")
        col5.metric("Potencia disipada (Pc)", f"{resultado['potencia']:.4f} W")


def pagina_historial():
    st.title("Historial de cálculos")

    try:
        registros = historial.leer_historial()
    except Exception as error:
        st.error("No se pudo leer el historial: " + str(error))
        return

    if not registros:
        st.info("Todavía no hay cálculos guardados.")
        return

    col1, col2 = st.columns(2)
    filtrar_fecha = col1.checkbox("Filtrar por fecha")
    fecha = col1.date_input("Fecha", disabled=not filtrar_fecha)
    material = col2.selectbox("Material", ["Todos"] + list(MATERIALES.keys()), key="filtro_material")

    filtrados = historial.filtrar_historial(registros, fecha if filtrar_fecha else None, material)

    if not filtrados:
        logger.warning("filtro sin coincidencias | material=%s", material)
        st.warning("No hay registros que coincidan con el filtro.")
        return

    filas = []
    for registro in iterar_historial(filtrados):
        entradas = registro.get("entradas", {})
        resultados = registro.get("resultados", {})
        filas.append({
            "ID": registro.get("id", ""),
            "Fecha": registro.get("fecha", ""),
            "Material": entradas.get("material", ""),
            "Tensión (V)": entradas.get("tension", ""),
            "Carga (Ω)": entradas.get("resistencia_carga", ""),
            "Longitud (m)": entradas.get("longitud_ida", ""),
            "Sección (mm²)": entradas.get("seccion", ""),
            "Rc (Ω)": round(resultados.get("rc", 0), 4),
            "Rt (Ω)": round(resultados.get("rt", 0), 4),
            "I (A)": round(resultados.get("corriente", 0), 4),
            "Vc (V)": round(resultados.get("caida_tension", 0), 4),
            "Pc (W)": round(resultados.get("potencia", 0), 4),
        })

    st.dataframe(filas, width="stretch")
    st.caption("Registros mostrados: " + str(len(filas)))


def pagina_logs():
    st.title("Logs del sistema")
    st.write("Eventos técnicos registrados por la aplicación.")

    lineas = logs.leer_logs_recientes(50)
    if not lineas:
        st.info("Todavía no hay eventos registrados.")
        return

    texto = "\n".join(iterar_logs(lineas))
    st.code(texto, language=None)


def pagina_fundamentos():
    st.title("Fundamentos y ayuda")

    st.subheader("Parámetros de entrada")
    st.markdown(
        "- **Tensión (V):** voltaje de la fuente. Debe ser mayor que cero.\n"
        "- **Resistencia de carga (Ω):** resistencia del dispositivo conectado.\n"
        "- **Material:** cobre, aluminio u otro material de la lista.\n"
        "- **Longitud de ida (m):** distancia entre la fuente y la carga.\n"
        "- **Sección transversal (mm²):** área del conductor, no el diámetro ni el calibre.\n"
    )

    st.subheader("Fórmulas")
    st.markdown(
        "1. Área en m²: A = A (mm²) × 10⁻⁶\n"
        "2. Longitud total: Ltotal = 2 × L\n"
        "3. Resistencia del cable: Rc = ρ × Ltotal / A\n"
        "4. Resistencia total: Rt = Rcarga + Rc\n"
        "5. Corriente: I = V / Rt\n"
        "6. Caída de tensión: Vc = I × Rc\n"
        "7. Potencia disipada: Pc = I² × Rc\n"
    )

    st.subheader("Ejemplo")
    st.write(
        "Con 12 V, 10 Ω, cobre, 5 m y 2,5 mm² se obtiene: "
        "Rc = 0,0672 Ω, Rt = 10,0672 Ω, I = 1,1920 A, "
        "Vc = 0,0801 V y Pc = 0,0955 W."
    )

    st.subheader("Supuestos y limitaciones")
    st.markdown(
        "- Se supone un circuito DC ideal a 20 °C.\n"
        "- El cable de ida y el de retorno tienen el mismo material, longitud y sección.\n"
        "- No se calcula ampacidad ni corriente máxima admisible.\n"
        "- No se considera calentamiento, resistencia de contactos ni otros efectos.\n"
        "- Es una simulación didáctica, no sirve para dimensionar instalaciones reales."
    )


def pagina_reportes():
    st.title("Reportes")
    st.write("Exporte los cálculos guardados a un archivo CSV.")

    try:
        registros = historial.leer_historial()
    except Exception as error:
        st.error("No se pudo leer el historial: " + str(error))
        return

    if not registros:
        st.info("Todavía no hay cálculos para exportar.")
        return

    opciones = {}
    for registro in iterar_historial(registros):
        entradas = registro.get("entradas", {})
        etiqueta = registro.get("id", "") + " | " + registro.get("fecha", "") + " | " + entradas.get("material", "")
        opciones[etiqueta] = registro

    seleccion = st.multiselect("Cálculos a exportar", list(opciones.keys()))

    if st.button("Exportar CSV"):
        if not seleccion:
            st.warning("Seleccione al menos un cálculo.")
        else:
            try:
                elegidos = [opciones[etiqueta] for etiqueta in seleccion]
                ruta = reportes.exportar_csv(elegidos)
                st.session_state["reporte"] = ruta
                st.success("Reporte creado en la carpeta reportes.")
            except Exception as error:
                logger.error("no se pudo exportar el reporte | %s", error)
                st.error("No se pudo exportar el reporte: " + str(error))

    ruta = st.session_state["reporte"] if "reporte" in st.session_state else None
    if ruta and os.path.exists(ruta):
        with open(ruta, "rb") as archivo:
            st.download_button(
                "Descargar CSV",
                data=archivo.read(),
                file_name=os.path.basename(ruta),
                mime="text/csv",
            )


st.sidebar.title("Calculadora DC")
pagina = st.sidebar.radio(
    "Navegación",
    ["Calculadora", "Historial", "Logs", "Fundamentos", "Reportes"],
)

if pagina == "Calculadora":
    pagina_calculadora()
elif pagina == "Historial":
    pagina_historial()
elif pagina == "Logs":
    pagina_logs()
elif pagina == "Fundamentos":
    pagina_fundamentos()
else:
    pagina_reportes()
