import streamlit as st
import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite
import os

# --- Cargar etiquetas desde labels.txt ---
try:
    with open("labels.txt", "r") as f:
        etiquetas = [line.strip().split(" ", 1)[1] for line in f.readlines()]
except Exception as e:
    st.error(f"❌ No se pudo leer labels.txt: {e}")
    st.stop()

# --- Cargar modelo TFLite ---
try:
    interpreter = tflite.Interpreter(model_path="model.tflite")
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
except Exception as e:
    st.error(f"❌ Error al cargar model.tflite: {e}")
    st.stop()

# --- Función para preparar imagen ---
def preparar_imagen(img):
    img = img.resize((224, 224)).convert("RGB")
    arr = np.array(img).astype(np.float32)
    arr = (arr / 127.5) - 1  # Normalización Teachable Machine
    return np.expand_dims(arr, axis=0)

# --- Interfaz Streamlit ---
st.set_page_config(page_title="Verificación de acceso", layout="centered")
st.title("🔐 Verificación de acceso con modelo TFLite")

texto = st.text_input("Escribe el comando (ej: abrir la puerta)")
imagen = st.file_uploader("Sube una imagen (jpg/png)", type=["jpg", "png"])
foto = st.camera_input("O toma una foto")

# --- Botón de verificación ---
if st.button("Verificar acceso"):
    if not texto or "abrir la puerta" not in texto.lower():
        st.error("❌ Comando incorrecto. Debes escribir: 'abrir la puerta'")
    elif not imagen and not foto:
        st.warning("⚠️ Debes subir o tomar una imagen.")
    else:
        img = Image.open(imagen if imagen else foto)
        entrada = preparar_imagen(img)

        try:
            interpreter.set_tensor(input_details[0]['index'], entrada)
            interpreter.invoke()
            salida = interpreter.get_tensor(output_details[0]['index'])[0]
        except Exception as e:
            st.error(f"❌ Error durante la inferencia: {e}")
            st.stop()

        clase = np.argmax(salida)
        confianza = np.max(salida)

        st.image(img, width=200)
        st.markdown(f"📊 **Resultado:** `{etiquetas[clase]}` ({confianza * 100:.2f}% de confianza)")

        if clase == 1:
            st.success("✅ Acceso concedido")
        else:
            st.error("❌ Acceso denegado")
