import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os
import platform

# --- Configuración de la app ---
st.set_page_config(page_title="Verificación de acceso", layout="centered")
st.title("🔐 Verificación de acceso a la casa")
st.write("Versión de Python:", platform.python_version())

# Entrada de texto para comando
texto = st.text_input("Escribe el comando para abrir la puerta (ej: abrir la puerta)")

# Subir imagen o tomar foto
imagen_cargada = st.file_uploader("Sube una imagen para verificar identidad", type=["jpg", "png"])
imagen_camara = None  # ✅ Se inicializa antes
imagen_camara = st.camera_input("Foto de acceso")

# --- Cargar modelo ---
model_path = 'keras_model.h5'
model = None
if os.path.exists(model_path):
    try:
        model = load_model(model_path)
    except Exception as e:
        st.error(f"❌ Error al cargar el modelo: {e}")
else:
    st.error(f"❌ Archivo del modelo no encontrado: {model_path}")

with st.sidebar:
    st.subheader("📷 Usa una foto para verificar si estás autorizado")

# --- Preparar imagen ---
def preparar_imagen(imagen):
    imagen = imagen.resize((224, 224))
    imagen = imagen.convert("RGB")
    img_array = np.array(imagen).astype(np.float32)
    normalized = (img_array / 127.0) - 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized
    return data

# --- Verificación al hacer clic ---
if st.button("Verificar acceso"):
    if model is None:
        st.error("❌ No se pudo cargar el modelo. La verificación no es posible.")
    elif not texto or "abrir la puerta" not in texto.lower():
        st.error("❌ Comando incorrecto. Debes escribir: 'abrir la puerta'")
    elif not imagen_cargada and not imagen_camara:
        st.warning("⚠️ Debes subir una imagen o tomar una foto.")
    else:
        if imagen_cargada:
            imagen = Image.open(imagen_cargada)
        else:
            imagen = Image.open(imagen_camara)

        datos = preparar_imagen(imagen)
        prediccion = model.predict(datos)

        if prediccion[0][0] > 0.5:
            st.success(f"✅ Persona Autorizada, con probabilidad: {prediccion[0][0]:.2f}")
        elif prediccion[0][1] > 0.5:
            st.error(f"❌ Persona No Autorizada, con probabilidad: {prediccion[0][1]:.2f}")
        else:
            st.warning("⚠️ No se pudo determinar la identidad con suficiente confianza.")
        st.image(imagen, width=200)
