import streamlit as st
import numpy as np
from PIL import Image
import os

# Verificar e instalar dependencias correctas
try:
    import tensorflow as tf
    from tensorflow.keras.models import load_model
except ImportError:
    st.error("Paquetes no encontrados. Instalando dependencias...")
    os.system("pip install tensorflow==2.10.0 protobuf==3.20.3")
    import tensorflow as tf
    from tensorflow.keras.models import load_model

# Configuración de la aplicación
st.set_page_config(page_title="Verificación de Acceso", layout="centered")
st.title("🔐 Sistema de Verificación Biométrica")

# Carga del modelo con manejo de errores
@st.cache_resource
def cargar_modelo_seguro():
    try:
        # Solución para problemas de capas custom
        custom_objects = {
            'DepthwiseConv2D': tf.keras.layers.DepthwiseConv2D
        }
        
        if not os.path.exists("keras_model.h5"):
            st.error("Archivo del modelo no encontrado")
            st.stop()
            
        model = load_model("keras_model.h5", 
                         custom_objects=custom_objects,
                         compile=False)
        return model
    except Exception as e:
        st.error(f"Error crítico: {str(e)}")
        st.error("Prueba ejecutar: pip install tensorflow==2.10.0 protobuf==3.20.3")
        st.stop()

model = cargar_modelo_seguro()

# Procesamiento de imágenes
def preparar_imagen(archivo_imagen):
    img = Image.open(archivo_imagen)
    img = img.resize((224, 224)).convert('RGB')
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

# Interfaz de usuario
with st.form("form_verificacion"):
    comando = st.text_input("Ingrese el comando de seguridad:")
    imagen = st.file_uploader("Cargar imagen de verificación", 
                             type=["jpg", "jpeg", "png"])
    
    if st.form_submit_button("Verificar Acceso"):
        if not comando or "abrir la puerta" not in comando.lower():
            st.error("Comando incorrecto")
        elif not imagen:
            st.warning("Debe cargar una imagen")
        else:
            try:
                # Procesamiento
                img_ready = preparar_imagen(imagen)
                
                # Predicción
                with st.spinner("Analizando..."):
                    pred = model.predict(img_ready)
                    clase = np.argmax(pred)
                    confianza = np.max(pred)
                
                # Resultados
                col1, col2 = st.columns(2)
                with col1:
                    st.image(imagen, width=200)
                with col2:
                    st.metric("Confianza", f"{confianza*100:.2f}%")
                
                if clase == 1 and confianza > 0.7:
                    st.success("✅ Verificación exitosa")
                    st.balloons()
                else:
                    st.error("❌ Acceso denegado")
                    
            except Exception as e:
                st.error(f"Error en procesamiento: {str(e)}")
