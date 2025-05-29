import streamlit as st
import tensorflow as tf
from tensorflow.keras.layers import DepthwiseConv2D
import numpy as np
from PIL import Image

# Solución para el error de DepthwiseConv2D
custom_objects = {'DepthwiseConv2D': DepthwiseConv2D}

@st.cache_resource
def cargar_modelo():
    try:
        model = tf.keras.models.load_model(
            "keras_model.h5",
            custom_objects=custom_objects,
            compile=False
        )
        return model
    except Exception as e:
        st.error(f"Error al cargar el modelo: {str(e)}")
        st.stop()

model = cargar_modelo()

# Resto del código permanece igual...
CLASS_NAMES = ["No autorizado", "Autorizado"]

def preprocess_image(image):
    img = Image.open(image)
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

# Interfaz de usuario
st.title("🔐 Sistema de Verificación")

password = st.text_input("Comando secreto:")
img_file = st.file_uploader("Imagen de verificación", type=["jpg", "png"])

if st.button("Verificar"):
    if not password or "abrir la puerta" not in password.lower():
        st.error("Comando incorrecto")
        st.stop()
    
    if not img_file:
        st.warning("Sube una imagen")
        st.stop()
    
    try:
        img = preprocess_image(img_file)
        prediction = model.predict(img)
        class_id = np.argmax(prediction)
        confidence = np.max(prediction)
        
        st.image(Image.open(img_file), width=200)
        st.write(f"Estado: {CLASS_NAMES[class_id]} ({confidence*100:.1f}%)")
        
        if class_id == 1 and confidence > 0.7:
            st.success("✅ Acceso concedido")
        else:
            st.error("❌ Acceso denegado")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
