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
st.write("Sube una imagen o toma una foto para comprobar si eres un usuario autorizado.")

model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

st.title("Reconocimiento de Imágenes")
#st.write("Versión de Python:", platform.python_version())
image = Image.open('OIG5.jpg')
st.image(image, width=350)
with st.sidebar:
    st.subheader("Usando un modelo entrenado en teachable Machine puedes Usarlo en esta app para identificar")
img_file_buffer = st.camera_input("Toma una Foto")

if img_file_buffer is not None:
    # To read image file buffer with OpenCV:
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
   #To read image file buffer as a PIL Image:
    img = Image.open(img_file_buffer)

    newsize = (224, 224)
    img = img.resize(newsize)
    # To convert PIL Image to numpy array:
    img_array = np.array(img)

    # Normalize the image
    normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    print(prediction)
    if prediction[0][0]>0.5:
      st.header('Persona Autorizada, con Probabilidad: '+str( prediction[0][0]) )
    if prediction[0][1]>0.5:
      st.header('Persona no autorizada, con Probabilidad: '+str( prediction[0][1]))
    #if prediction[0][2]>0.5:
    # st.header('Derecha, con Probabilidad: '+str( prediction[0][2]))


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
