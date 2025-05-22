import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf

# --- Cargar modelo de Keras ---
@st.cache_resource
def cargar_modelo():
    modelo = tf.keras.models.load_model("modelo.h5")
    return modelo

modelo = cargar_modelo()

# --- Preprocesamiento de imagen ---
def preparar_imagen(imagen, tamaño=(224, 224)):
    imagen = imagen.resize(tamaño)
    imagen = imagen.convert("RGB")
    imagen = np.array(imagen) / 255.0
    imagen = np.expand_dims(imagen, axis=0)
    return imagen

# --- Interfaz Streamlit ---
st.set_page_config(page_title="Acceso con Reconocimiento Facial", layout="centered")
st.title("🔐 Acceso Inteligente con Keras + Streamlit")
st.write("Reconocimiento facial con modelo de Keras para autorizar el acceso.")

# Paso 1: Entrada de texto
st.header("Paso 1: Escribe el comando")
texto_ingresado = st.text_input("Comando (ejemplo: abrir la puerta)")

# Paso 2: Cargar imagen
st.header("Paso 2: Carga tu imagen para verificación")
imagen_usuario = st.file_uploader("Sube una imagen (jpg o png)", type=["jpg", "png"])

# Verificación
if st.button("Verificar acceso"):
    if not texto_ingresado:
        st.warning("⚠️ Primero escribe el comando.")
    elif not imagen_usuario:
        st.warning("⚠️ Debes subir una imagen.")
    elif "abrir la puerta" not in texto_ingresado.lower():
        st.error("❌ Comando incorrecto. Usa exactamente: 'abrir la puerta'")
    else:
        imagen = Image.open(imagen_usuario)
        imagen_preparada = preparar_imagen(imagen)

        # Predicción
        prediccion = modelo.predict(imagen_preparada)
        clase = np.argmax(prediccion, axis=1)[0]  # 0 o 1

        if clase == 1:  # Suponiendo que 1 es 'autorizado'
            st.success("✅ Acceso concedido. ¡Puerta abierta!")
            st.image(imagen, caption="Usuario autorizado", width=200)
        else:
            st.error("❌ Acceso denegado. Usuario no reconocido.")
