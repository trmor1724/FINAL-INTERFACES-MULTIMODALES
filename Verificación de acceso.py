import streamlit as st
from PIL import Image

# Configuración de la app
st.set_page_config(page_title="Control de Acceso Inteligente", layout="centered")
st.title("🔐 Acceso Inteligente con Texto + Carga de Imagen")
st.write("Simula el acceso a una puerta con comando por texto y carga de imagen.")

# --- Entrada de texto ---
st.header("Paso 1: Escribe el comando de acceso")
texto_ingresado = st.text_input("Comando (ejemplo: abrir la puerta)")

# --- Cargar imagen ---
st.header("Paso 2: Carga tu imagen")
imagen_usuario = st.file_uploader("Sube una imagen (jpg o png)", type=["jpg", "png"])

# --- Verificar acceso ---
if st.button("Verificar acceso"):
    if not texto_ingresado:
        st.warning("⚠️ Primero escribe un comando.")
    elif not imagen_usuario:
        st.warning("⚠️ Debes subir una imagen.")
    else:
        if "abrir la puerta" in texto_ingresado.lower():
            st.success("✅ Acceso concedido. ¡Puerta abierta!")
            imagen = Image.open(imagen_usuario)
            st.image(imagen, caption="Imagen recibida", width=200)
        else:
            st.error("❌ Comando incorrecto. Debes escribir exactamente: 'abrir la puerta'")
