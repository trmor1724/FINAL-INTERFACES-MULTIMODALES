import streamlit as st
import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite
import os

# Configuración segura para Streamlit Cloud
try:
    st.set_page_config(
        page_title="Verificación Biométrica",
        page_icon="🔐",
        layout="centered"
    )
except:
    st.warning("Error menor en configuración de página")

# Verificación de archivos esenciales
ESSENTIAL_FILES = {
    "model.tflite": "Modelo de reconocimiento",
    "labels.txt": "Etiquetas de clasificación"
}

for file, desc in ESSENTIAL_FILES.items():
    if not os.path.exists(file):
        st.error(f"ARCHIVO FALTANTE: {file} ({desc})")
        st.stop()

# Cargar etiquetas
try:
    with open("labels.txt", "r", encoding="utf-8") as f:
        labels = [line.strip().split(" ", 1)[1] for line in f.readlines()]
except Exception as e:
    st.error(f"ERROR EN LABELS: {str(e)}")
    st.stop()

# Inicialización del modelo TFLite
@st.cache_resource
def load_tflite_model():
    try:
        interpreter = tflite.Interpreter(model_path="model.tflite")
        interpreter.allocate_tensors()
        return interpreter
    except Exception as e:
        st.error(f"ERROR EN MODELO: {str(e)}")
        st.stop()

model = load_tflite_model()

# Procesamiento de imágenes optimizado
def process_image(upload):
    try:
        img = Image.open(upload).convert("RGB").resize((224, 224))
        return (np.array(img, dtype=np.float32) / 127.5) - 1.0
    except Exception as e:
        st.error(f"ERROR EN IMAGEN: {str(e)}")
        return None

# Interfaz de usuario
st.title("🔒 Sistema de Autenticación Biométrica")

with st.form("auth_form"):
    command = st.text_input("Frase de acceso:", placeholder="Ej: abrir la puerta")
    image = st.file_uploader("Imagen de identidad:", type=["jpg", "png", "jpeg"])
    
    if st.form_submit_button("Validar Identidad"):
        if not command or "abrir la puerta" not in command.lower():
            st.error("❌ Frase incorrecta. Use: 'abrir la puerta'")
        elif not image:
            st.warning("⚠️ Suba una imagen de identificación")
        else:
            input_data = process_image(image)
            if input_data is not None:
                try:
                    # Configurar entrada/salida del modelo
                    input_details = model.get_input_details()
                    output_details = model.get_output_details()
                    
                    # Inferencia
                    model.set_tensor(input_details[0]['index'], np.expand_dims(input_data, axis=0))
                    model.invoke()
                    results = model.get_tensor(output_details[0]['index'])[0]
                    
                    # Resultados
                    confidence = np.max(results)
                    class_id = np.argmax(results)
                    
                    st.image(image, width=200)
                    st.metric("Confianza", f"{confidence*100:.2f}%")
                    
                    if class_id == 1 and confidence > 0.7:
                        st.success("✅ Identidad confirmada - Acceso autorizado")
                    else:
                        st.error("❌ Identidad no reconocida - Acceso denegado")
                        
                except Exception as e:
                    st.error(f"ERROR EN INFERENCIA: {str(e)}")
