import streamlit as st
import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite
import os

st.set_page_config(page_title="Verificación Biométrica", layout="centered")
st.title("🔐 Verificación de acceso con modelo TFLite")

if not os.path.exists("model.tflite"):
    st.error("❌ Falta el archivo 'model.tflite'. Agrégalo al proyecto.")
    st.stop()

if not os.path.exists("labels.txt"):
    st.error("❌ Falta el archivo 'labels.txt'.")
    st.stop()

with open("labels.txt", "r", encoding="utf-8") as f:
    labels = [line.strip().split(" ", 1)[1] for line in f]

@st.cache_resource
def cargar_modelo():
    interpreter = tflite.Interpreter(model_path="model.tflite")
    interpreter.allocate_tensors()
    return interpreter

interpreter = cargar_modelo()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def procesar_imagen(uploaded_file):
    img = Image.open(uploaded_file).convert("RGB").resize((224, 224))
    img_array = np.array(img).astype(np.float32)
    normalizado = (img_array / 127.5) - 1
    return np.expand_dims(normalizado, axis=0), img

texto = st.text_input("🔑 Comando de voz/texto:", placeholder="Ej: abrir la puerta")
imagen = st.file_uploader("📷 Imagen de identificación:", type=["jpg", "png", "jpeg"])
foto = st.camera_input("O usa tu cámara")

if st.button("🔍 Verificar"):
    if "abrir la puerta" not in texto.lower():
        st.error("❌ Comando incorrecto. Usa 'abrir la puerta'")
    elif not imagen and not foto:
        st.warning("⚠️ Por favor sube una imagen o toma una foto.")
    else:
        input_data, preview = procesar_imagen(imagen or foto)
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        resultado = interpreter.get_tensor(output_details[0]['index'])[0]

        pred = np.argmax(resultado)
        conf = np.max(resultado)

        st.image(preview, width=200)
        st.metric("Confianza", f"{conf*100:.2f}%")
        st.success(f"Predicción: {labels[pred]}")

        if pred == 1 and conf > 0.7:
            st.success("✅ Acceso autorizado")
        else:
            st.error("❌ Acceso denegado")
