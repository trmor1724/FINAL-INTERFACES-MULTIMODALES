import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import platform

# --- Configuración de la app ---
st.set_page_config(page_title="Verificación de acceso", layout="centered")
st.title("🔐 Verificación de acceso con Teachable Machine")

# Mostrar versión de Python
st.write("Versión de Python:", platform.python_version())

# Entrada de texto para comando
texto = st.text_input("Escribe el comando para abrir la puerta (ej: abrir la puerta)")

# Subir imagen o tomar foto
imagen_cargada = st.file_uploader("Sube una imagen para verificar identidad", type=["jpg", "png"])
imagen_camara = st.camera_input("O toma una foto con la cámara")
st.write("Sube una imagen o toma una foto para comprobar si eres un usuario autorizado.")

# Procesamiento de imagen para modelo Teachable Machine (224x224)
def preparar_imagen(imagen):
    imagen = imagen.resize((224, 224))
    imagen = imagen.convert("RGB")
    imagen_array = np.array(imagen).astype(np.float32)
    # Normalización que espera el modelo
    imagen_normalizada = (imagen_array / 127.0) - 1
    imagen_normalizada = np.expand_dims(imagen_normalizada, axis=0)
    return imagen_normalizada

# Etiquetas (ajusta según tu modelo)
etiquetas = ["No autorizado", "Autorizado"]  # Ajusta según tu modelo

def predecir(imagen):
    imagen_preparada = preparar_imagen(imagen)
    prediccion = model.predict(imagen_preparada)
    clase = np.argmax(prediccion)
    confianza = np.max(prediccion)
    return clase, confianza, prediccion

# Verificación al hacer clic
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

        clase, confianza, prediccion = predecir(imagen)

        st.write(f"📊 Predicción: **{etiquetas[clase]}** con {confianza*100:.2f}% de confianza.")
        st.write(f"Detalles predicción cruda: {prediccion}")

        if clase == 1:  # Autorizado
            st.success("✅ Acceso concedido. ¡Bienvenido!")
            st.image(imagen, width=200)
        else:
            st.error("❌ Acceso denegado. No autorizado.")
