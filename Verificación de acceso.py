import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# --- Cargar el modelo de Teachable Machine ---
@st.cache_resource
def cargar_modelo():
    model = tf.keras.models.load_model("keras_model.h5")
    return model

model = cargar_modelo()

# --- Configuración de la app ---
st.set_page_config(page_title="Verificación de acceso", layout="centered")
st.title("🔐 Verificación de acceso con Teachable Machine")
st.write("Sube una imagen para comprobar si eres un usuario autorizado.")

# Entrada de texto
texto = st.text_input("Escribe el comando para abrir la puerta (ej: abrir la puerta)")

# Cargar imagen
imagen_cargada = st.file_uploader("Sube una imagen para verificar identidad", type=["jpg", "png"])

# Procesamiento de imagen para modelo Teachable Machine (224x224)
def preparar_imagen(imagen):
    imagen = imagen.resize((224, 224))
    imagen = imagen.convert("RGB")
    imagen = np.array(imagen) / 255.0
    imagen = np.expand_dims(imagen, axis=0)
    return imagen

# Etiquetas (ajusta según tu modelo)
etiquetas = ["No autorizado", "Autorizado"]  # Teachable Machine generalmente da output como softmax

# Verificación
if st.button("Verificar acceso"):
    if not texto or "abrir la puerta" not in texto.lower():
        st.error("❌ Comando incorrecto. Debes escribir: 'abrir la puerta'")
    elif not imagen_cargada:
        st.warning("⚠️ Debes subir una imagen.")
    else:
        imagen = Image.open(imagen_cargada)
        imagen_procesada = preparar_imagen(imagen)

        prediccion = model.predict(imagen_procesada)
        clase = np.argmax(prediccion)
        confianza = np.max(prediccion)

        st.write(f"📊 Predicción: **{etiquetas[clase]}** con {confianza*100:.2f}% de confianza.")

        if clase == 1:  # Autorizado
            st.success("✅ Acceso concedido. ¡Bienvenido!")
            st.image(imagen, width=200)
        else:
            st.error("❌ Acceso denegado. No autorizado.")
