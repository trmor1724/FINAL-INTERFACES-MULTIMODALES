import streamlit as st
import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite

# Leer etiquetas desde archivo
with open("labels.txt", "r") as f:
    etiquetas = [line.strip().split(' ', 1)[1] for line in f.readlines()]

# Cargar modelo TFLite
interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def preparar_imagen(img):
    img = img.resize((224, 224)).convert("RGB")
    arr = np.array(img).astype(np.float32)
    arr = (arr / 127.5) - 1  # Normalización para Teachable Machine
    return np.expand_dims(arr, axis=0)

st.set_page_config(page_title="Verificación de acceso", layout="centered")
st.title("🔐 Verificación de acceso con modelo TFLite")

texto = st.text_input("Escribe el comando (ej: abrir la puerta)")
imagen = st.file_uploader("Sube una imagen (jpg/png)", type=["jpg", "png"])

if st.button("Verificar acceso"):
    if not texto or "abrir la puerta" not in texto.lower():
        st.error("❌ Comando incorrecto. Usa: 'abrir la puerta'")
    elif not imagen:
        st.warning("⚠️ Debes subir una imagen.")
    else:
        img = Image.open(imagen)
        entrada = preparar_imagen(img)

        interpreter.set_tensor(input_details[0]['index'], entrada)
        interpreter.invoke()
        salida = interpreter.get_tensor(output_details[0]['index'])[0]

        clase = np.argmax(salida)
        confianza = np.max(salida)

        st.image(img, width=200)
        st.write(f"📊 Resultado: **{etiquetas[clase]}** con {confianza*100:.2f}% de confianza")
        if clase == 0:
            st.success("✅ Acceso concedido")
        else:
            st.error("❌ Acceso denegado")
