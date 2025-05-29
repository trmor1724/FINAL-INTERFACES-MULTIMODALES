import streamlit as st
import numpy as np
from PIL import Image as Image, ImageOps as ImagOps
from keras.models import load_model
import platform

# Mostrar versión del entorno
st.write("🔧 Versión de Python:", platform.python_version())

# Cargar etiquetas desde labels.txt
with open("labels.txt", "r", encoding="utf-8") as f:
    etiquetas = [line.strip().split(" ", 1)[1] for line in f.readlines()]

# Cargar modelo
model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Título
st.title("🏠 Verificación de acceso - Casa Inteligente")

with st.sidebar:
    st.subheader("🔐 Reconocimiento de acceso")
    st.markdown("""
    Este sistema identifica si la persona que aparece en la cámara está autorizada para ingresar a la casa.  
    Basado en un modelo de Teachable Machine entrenado con imágenes de personas autorizadas y no autorizadas.
    """)

# Captura de imagen desde cámara
img_file_buffer = st.camera_input("📸 Toma una foto para verificar identidad")

if img_file_buffer is not None:
    img = Image.open(img_file_buffer).resize((224, 224)).convert("RGB")
    img_array = np.array(img)
    normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array

    prediction = model.predict(data)
    clase = np.argmax(prediction)
    probabilidad = np.max(prediction)

    st.image(img, caption="📷 Imagen capturada", width=200)
    st.metric("🔍 Confianza del modelo", f"{probabilidad*100:.2f}%")
    st.markdown(f"🧠 Resultado del modelo: **{etiquetas[clase]}**")

    # Clasificación basada en etiquetas (0 = Autorizado)
    if clase == 0 and probabilidad > 0.6:
        st.success("✅ Acceso concedido – Persona autorizada")
    else:
        st.error("❌ Acceso denegado – Persona no autorizada")
