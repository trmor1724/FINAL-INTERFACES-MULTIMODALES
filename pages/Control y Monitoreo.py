import streamlit as st
import pandas as pd
from datetime import datetime

# --- Simulación de estado de la puerta y registros ---
if "estado_puerta" not in st.session_state:
    st.session_state.estado_puerta = " "
if "registros" not in st.session_state:
    st.session_state.registros = []
if "modo" not in st.session_state:
    st.session_state.modo = "Día"

# --- Título de la app ---
st.set_page_config(page_title="Control y Monitoreo", layout="centered")
st.title("🚪 Panel de Control y Monitoreo del Acceso")

# --- Estado actual de la puerta ---
st.subheader("🔒 Estado actual de la puerta:")
st.info(f"**{st.session_state.estado_puerta}**")

# --- Botones de control manual ---
st.subheader("🎮 Control manual:")
col1, col2 = st.columns(2)

with col1:
    if st.button("🔐 Cerrar puerta"):
        st.session_state.estado_puerta = "Cerrada"
        st.session_state.registros.append(
            {"Fecha": datetime.now(), "Acción": "Puerta cerrada manualmente", "Método": "Botón"}
        )

with col2:
    if st.button("🔓 Abrir puerta"):
        st.session_state.estado_puerta = "Abierta"
        st.session_state.registros.append(
            {"Fecha": datetime.now(), "Acción": "Puerta abierta manualmente", "Método": "Botón"}
        )

# --- Activar alarma (simulación) ---
if st.button("🚨 Activar alarma"):
    st.warning("⚠️ ¡Alarma activada!")
    st.session_state.registros.append(
        {"Fecha": datetime.now(), "Acción": "Alarma activada", "Método": "Botón"}
    )

# --- Selección de modo día/noche ---
st.subheader("🌗 Modo del sistema:")
modo = st.radio("Selecciona el modo:", ["Día", "Noche"], horizontal=True)
st.session_state.modo = modo
st.success(f"Modo actual: **{st.session_state.modo}**")

# --- Mostrar registros de acceso ---
st.subheader("📜 Registro de accesos:")
if st.session_state.registros:
    df = pd.DataFrame(st.session_state.registros)
    df["Fecha"] = pd.to_datetime(df["Fecha"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    st.dataframe(df[::-1], use_container_width=True)
else:
    st.write("No hay registros aún.")
