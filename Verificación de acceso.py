import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os

# --- Configuración inicial ---
st.set_page_config(page_title="Verificación de acceso", layout="centered")
st.title("🔐 Verificación de acceso con IA")

# --- Verificar y cargar el modelo ---
@st.cache_resource
def cargar_modelo():
    # Verificar si el archivo existe
    if not os.path.exists("keras_model.h5"):
        st.error("ERROR: No se encuentra 'keras_model.h5'")
        st.stop()
    
    try:
        # Cargar modelo con compatibilidad para diferentes versiones de TF
        model = tf.keras.models.load_model("keras_model.h5", compile=False)
        return model
    except Exception as e:
        st.error(f"Error al cargar el modelo: {str(e)}")
        st.stop()

model = cargar_modelo()

# --- Definir etiquetas ---
CLASS_NAMES = ["No autorizado", "Autorizado"]  # Ajustar según tu modelo

# --- Función de preprocesamiento ---
def preprocess_image(image):
    img = Image.open(image)
    img = img.resize((224, 224))  # Tamaño requerido por Teachable Machine
    img_array = np.array(img) / 255.0  # Normalización
    img_array = np.expand_dims(img_array, axis=0)  # Añadir dimensión batch
    return img_array

# --- Interfaz de usuario ---
st.subheader("Autenticación de dos factores")

# 1. Factor de conocimiento (contraseña)
password = st.text_input("Escribe el comando secreto:")

# 2. Factor de posesión (imagen biométrica)
uploaded_file = st.file_uploader("Sube tu imagen de verificación", 
                               type=["jpg", "jpeg", "png"])
camera_image = st.camera_input("O toma una foto ahora")

# --- Procesamiento ---
if st.button("Verificar acceso", type="primary"):
    # Validar contraseña
    if not password or "abrir la puerta" not in password.lower():
        st.error("Comando incorrecto. Intenta con: 'abrir la puerta'")
        st.stop()
    
    # Obtener imagen (prioridad: cámara > archivo)
    image_source = camera_image if camera_image is not None else uploaded_file
    
    if image_source is None:
        st.warning("Debes subir una imagen o tomar una foto")
        st.stop()
    
    try:
        # Preprocesar imagen
        img_array = preprocess_image(image_source)
        
        # Mostrar imagen
        st.image(Image.open(image_source), 
                caption="Imagen de verificación",
                width=200)
        
        # Realizar predicción
        with st.spinner("Verificando identidad..."):
            predictions = model.predict(img_array)
            confidence = np.max(predictions)
            class_id = np.argmax(predictions)
            
            st.progress(int(confidence * 100))
            
            # Mostrar resultados
            st.subheader(f"Resultado: {CLASS_NAMES[class_id]}")
            st.write(f"Confianza: {confidence*100:.2f}%")
            
            # Tomar decisión
            if class_id == 1 and confidence > 0.7:  # Umbral ajustable
                st.success("✅ Acceso concedido")
                st.balloons()
            else:
                st.error("❌ Acceso denegado")
                
    except Exception as e:
        st.error(f"Error en el procesamiento: {str(e)}")
