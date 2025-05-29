import streamlit as st
import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite
import os

# --- Configuración segura para Streamlit Cloud ---
st.set_page_config(page_title="Verificación de Acceso", layout="centered")

# --- Verificar archivos críticos ---
REQUIRED_FILES = ["model.tflite", "labels.txt"]
for file in REQUIRED_FILES:
    if not os.path.exists(file):
        st.error(f"❌ Error: Archivo {file} no encontrado")
        st.stop()

# --- Cargar etiquetas ---
with open("labels.txt", "r") as f:
    etiquetas = [line.strip().split(" ", 1)[1] for line in f.readlines()]

# --- Cargar modelo TFLite (más ligero que Keras) ---
try:
    interpreter = tflite.Interpreter(model_path="model.tflite")
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
except Exception as e:
    st.error(f"❌ Error al cargar el modelo: {str(e)}")
    st.stop()

# --- Función de preprocesamiento optimizada ---
def procesar_imagen(imagen):
    img = Image.open(imagen).resize((224, 224)).convert("RGB")
    return (np.array(img, dtype=np.float32) / 127.5 - 1.0

# --- Interfaz de usuario ---
st.title("🔐 Sistema de Verificación Biométrica")

with st.form("acceso_form"):
    comando = st.text_input("Comando de seguridad:")
    imagen = st.file_uploader("Sube tu imagen", type=["jpg", "png", "jpeg"])
    
    if st.form_submit_button("Verificar"):
        if not comando or "abrir la puerta" not in comando.lower():
            st.error("Comando inválido. Intenta: 'abrir la puerta'")
        elif not imagen:
            st.warning("Debes subir una imagen")
        else:
            try:
                # Preprocesamiento
                input_data = np.expand_dims(procesar_imagen(imagen), axis=0)
                
                # Inferencia
                interpreter.set_tensor(input_details[0]['index'], input_data)
                interpreter.invoke()
                resultados = interpreter.get_tensor(output_details[0]['index'])[0]
                
                # Resultados
                confianza = np.max(resultados)
                clase = np.argmax(resultados)
                
                st.image(Image.open(imagen), width=200)
                st.write(f"**Predicción:** {etiquetas[clase]} ({confianza*100:.2f}%)")
                
                st.success("✅ Acceso concedido") if clase == 1 else st.error("❌ Acceso denegado")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
