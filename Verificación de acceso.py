import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os

# --- Verificar existencia del modelo ---
if not os.path.exists("keras_model.h5"):
    st.error("❌ Error: El archivo 'keras_model.h5' no existe en el directorio actual")
    st.stop()

# --- Cargar el modelo de Teachable Machine con manejo de errores ---
@st.cache_resource
def cargar_modelo():
    try:
        # Intenta cargar con la API moderna primero
        model = tf.keras.models.load_model("keras_model.h5", compile=False)
        st.success("✅ Modelo cargado correctamente")
        return model
    except Exception as e:
        st.error(f"❌ Error al cargar el modelo: {str(e)}")
        st.error("Posibles soluciones:")
        st.error("1. Verifica que el modelo fue exportado correctamente desde Teachable Machine")
        st.error("2. Asegúrate de usar TensorFlow 2.x")
        st.error("3. Revisa que el archivo no esté corrupto")
        st.stop()

try:
    model = cargar_modelo()
except Exception as e:
    st.error(f"❌ Error inesperado: {str(e)}")
    st.stop()

# --- Configuración de la app ---
st.set_page_config(page_title="Verificación de acceso", layout="centered")
st.title("🔐 Verificación de acceso con Teachable Machine")

# --- Etiquetas (deben coincidir con tu entrenamiento) ---
etiquetas = ["No autorizado", "Autorizado"]  # Ajusta según tu modelo

# --- Interfaz de usuario ---
texto = st.text_input("Escribe el comando para abrir la puerta (ej: abrir la puerta)")
imagen_cargada = st.file_uploader("Sube una imagen para verificar identidad", type=["jpg", "jpeg", "png"])

# --- Procesamiento de imagen ---
def preparar_imagen(imagen):
    try:
        img = Image.open(imagen)
        img = img.resize((224, 224))  # Tamaño esperado por Teachable Machine
        img_array = np.array(img) / 255.0  # Normalización
        img_array = np.expand_dims(img_array, axis=0)  # Añadir dimensión batch
        return img_array
    except Exception as e:
        st.error(f"❌ Error al procesar imagen: {str(e)}")
        return None

# --- Verificación ---
if st.button("Verificar acceso"):
    # Validación de entrada
    if not texto or "abrir la puerta" not in texto.lower():
        st.error("❌ Comando incorrecto. Debes escribir: 'abrir la puerta'")
    elif not imagen_cargada:
        st.warning("⚠️ Debes subir una imagen.")
    else:
        # Procesar imagen
        imagen_procesada = preparar_imagen(imagen_cargada)
        if imagen_procesada is None:
            st.stop()
        
        # Mostrar imagen
        st.image(Image.open(imagen_cargada), width=200, caption="Imagen subida")
        
        # Predecir
        try:
            with st.spinner("🔍 Analizando imagen..."):
                prediccion = model.predict(imagen_procesada)
                clase = np.argmax(prediccion)
                confianza = np.max(prediccion)
                
                st.write(f"📊 Resultado: **{etiquetas[clase]}** ({confianza*100:.2f}% de confianza)")
                
                if clase == 1:  # Autorizado
                    st.success("✅ Acceso concedido. ¡Bienvenido!")
                else:
                    st.error("❌ Acceso denegado. No autorizado.")
                    
        except Exception as e:
            st.error(f"❌ Error durante la predicción: {str(e)}")
            st.success("✅ Acceso concedido. ¡Bienvenido!")
            st.image(imagen, width=200)
        else:
            st.error("❌ Acceso denegado. No autorizado.")
