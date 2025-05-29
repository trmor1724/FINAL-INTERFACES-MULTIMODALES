import streamlit as st
import numpy as np
from PIL import Image as Image, ImageOps as ImagOps
from keras.models import load_model
import platform

# Mostrar versión del entorno
st.write("🔧 Versión de Python:", platform.python_version())

# Cargar modelo entrenado desde Teachable Machine
model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Título de la app
st.title("🏠 Sistema de Casa Inteligente")

# Descripción general
with st.sidebar:
    st.subheader("📷 Reconocimiento de gestos para control del hogar")
    st.markdown("""
    Esta aplicación utiliza un modelo entrenado con Teachable Machine para reconocer gestos realizados frente a una cámara.  
    Puedes usarla para controlar funciones de una casa inteligente, como abrir puertas, encender luces o activar alarmas.
    """)

# Entrada de cámara
img_file_buffer = st.camera_input("📸 Realiza un gesto frente a la cámara")

if img_file_buffer is not None:
    # Procesar imagen capturada
    img = Image.open(img_file_buffer).resize((224, 224)).convert("RGB")
    img_array = np.array(img)
    normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array

    # Hacer predicción
    prediction = model.predict(data)

    # Mostrar resultado
    st.image(img, caption="Imagen capturada", width=200)

    if prediction[0][0] > 0.5:
        st.success(f"📥 Gesto detectado: **Izquierda** – podría indicar cerrar persiana o apagar luz")
        st.metric("Probabilidad", f"{prediction[0][0]*100:.2f}%")
    if prediction[0][1] > 0.5:
        st.success(f"📤 Gesto detectado: **Arriba** – podría indicar abrir puerta o encender ventilador")
        st.metric("Probabilidad", f"{prediction[0][1]*100:.2f}%")
    # Descomenta si tu modelo tiene más gestos:
    # if prediction[0][2] > 0.5:
    #     st.success(f"Gesto detectado: Derecha – acción personalizada")
