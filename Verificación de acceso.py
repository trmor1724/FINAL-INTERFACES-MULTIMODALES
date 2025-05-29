import streamlit as st
import numpy as np
from PIL import Image
import os

# Solución alternativa si tflite_runtime no está disponible
try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    st.warning("tflite_runtime no encontrado, usando TensorFlow Lite")
    import tensorflow as tf
    tflite = tf.lite

# Configuración de la aplicación
st.set_page_config(
    page_title="Verificación de Acceso",
    layout="centered",
    page_icon="🔒"
)

# Verificación de archivos esenciales
if not os.path.exists("model.tflite"):
    st.error("❌ Error: Archivo model.tflite no encontrado")
    st.stop()

if not os.path.exists("labels.txt"):
    st.error("❌ Error: Archivo labels.txt no encontrado")
    st.stop()

# Cargar etiquetas
with open("labels.txt", "r") as f:
    labels = [line.strip().split(" ", 1)[1] for line in f.readlines()]

# Cargar modelo
@st.cache_resource
def load_model():
    try:
        interpreter = tflite.Interpreter(model_path="model.tflite")
        interpreter.allocate_tensors()
        return interpreter
    except Exception as e:
        st.error(f"❌ Error al cargar el modelo: {str(e)}")
        st.stop()

model = load_model()

# Interfaz de usuario
st.title("🔐 Sistema de Verificación Biométrica")

with st.form("auth_form"):
    command = st.text_input("Ingrese el comando de seguridad:")
    image = st.file_uploader("Suba su imagen de identificación", type=["jpg", "png", "jpeg"])
    
    if st.form_submit_button("Verificar Acceso"):
        if not command or "abrir la puerta" not in command.lower():
            st.error("Comando incorrecto. Use: 'abrir la puerta'")
        elif not image:
            st.warning("Debe subir una imagen")
        else:
            try:
                # Preprocesamiento
                img = Image.open(image).resize((224, 224)).convert("RGB")
                input_data = (np.array(img, dtype=np.float32) / 127.5) - 1.0
                input_data = np.expand_dims(input_data, axis=0)
                
                # Inferencia
                input_details = model.get_input_details()
                output_details = model.get_output_details()
                
                model.set_tensor(input_details[0]['index'], input_data)
                model.invoke()
                results = model.get_tensor(output_details[0]['index'])[0]
                
                # Resultados
                confidence = np.max(results)
                class_id = np.argmax(results)
                
                st.image(img, width=200)
                st.write(f"**Resultado:** {labels[class_id]} ({confidence*100:.2f}% confianza)")
                
                if class_id == 1 and confidence > 0.7:
                    st.success("✅ Acceso concedido")
                else:
                    st.error("❌ Acceso denegado")
                    
            except Exception as e:
                st.error(f"Error en procesamiento: {str(e)}")
