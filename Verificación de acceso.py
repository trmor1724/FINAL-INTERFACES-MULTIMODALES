import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf  # <-- Este requiere que lo instales vía requirements.txt

# Cargar modelo
@st.cache_resource
def cargar_modelo():
    modelo = tf.keras.models.load_model("modelo.h5")
    return modelo

modelo = cargar_modelo()

# Preprocesamiento
def preparar_imagen(imagen, tamaño=(224, 224)):
    imagen = imagen.resize(tamaño)
    imagen = imagen.convert("RGB")
    imagen = np.array(imagen) / 255.0
    imagen = np.expand_dims(imagen, axis=0)
    return imagen

# Interfaz
st.set_page_config(page_title="Acceso con Reconocimiento Facial", layout="centered")
st.title("🔐 Acceso Inteligente con Keras + Streamlit")

texto_ingresado = st.text_input("Comando (ejemplo: abrir la puerta)")
imagen_usuario = st.file_uploader("Sube una imagen (jpg o png)", type=["jpg", "png"])

if st.button("Verificar acceso"):
    if not texto_ingresado or not imagen_usuario:
        st.warning("⚠️ Escribe el comando y sube una imagen.")
    elif "abrir la puerta" not in texto_ingresado.lower():
        st.error("❌ Comando incorrecto. Usa 'abrir la puerta'")
    else:
        imagen = Image.open(imagen_usuario)
        imagen_preparada = preparar_imagen(imagen)
        prediccion = modelo.predict(imagen_preparada)
        clase = np.argmax(prediccion, axis=1)[0]

        if clase == 1:
            st.success("✅ Acceso concedido. ¡Puerta abierta!")
            st.image(imagen, caption="Usuario autorizado", width=200)
        else:
            st.error("❌ Acceso denegado. Usuario no reconocido.")
