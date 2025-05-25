import streamlit as st
import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite

# Cargar modelo TFLite
@st.cache_resource
def cargar_modelo():
    interpreter = tflite.Interpreter(model_path="model.tflite")
    interpreter.allocate_tensors()
    return interpreter

interpreter = cargar_modelo()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Leer etiquetas
with open("labels.txt", "r") as f:
    etiquetas = [line.strip().split(" ", 1)[1] for line in f]

st.title("🔐 Verificación de acceso (TFLite)")
texto = st.text_input("Comando (ej: abrir la puerta)")
imagen = st.file_uploader("Imagen", type=["jpg", "png"])

def preparar_imagen(img):
    img = img.resize((224, 224)).convert("RGB")
    arr = np.array(img).astype(np.float32)
    arr = (arr / 127.5) - 1
    return np.expand_dims(arr, axis=0)

if st.button("Verificar"):
    if not texto or "abrir la puerta" not in texto.lower():
        st.error("Comando inválido")
    elif not imagen:
        st.warning("Sube una imagen")
    else:
        img = Image.open(imagen)
        entrada = preparar_imagen(img)
        interpreter.set_tensor(input_details[0]['index'], entrada)
        interpreter.invoke()
        resultado = interpreter.get_tensor(output_details[0]['index'])[0]

        clase = np.argmax(resultado)
        confianza = np.max(resultado)

        st.image(img, width=200)
        st.write(f"Predicción: **{etiquetas[clase]}** ({confianza*100:.2f}%)")
        if clase == 0:
            st.success("✅ Acceso concedido")
        else:
            st.error("❌ Acceso denegado")
