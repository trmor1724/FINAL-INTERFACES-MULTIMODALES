import streamlit as st
import speech_recognition as sr
from PIL import Image
import numpy as np
import cv2
import os

# Configuración de la app
st.set_page_config(page_title="Control de Acceso Inteligente", layout="centered")
st.title("🔐 Acceso Inteligente con Voz + Reconocimiento Facial")

st.write("Simula el acceso a una puerta con texto o voz y carga de imagen.")

# --- Entrada de texto o voz ---
st.header("Paso 1: ¿Cómo deseas pedir acceso?")
opcion_entrada = st.radio("Selecciona método:", ["Texto", "Voz"])

if opcion_entrada == "Texto":
    texto_ingresado = st.text_input("Escribe el comando (ej: abrir la puerta)")
elif opcion_entrada == "Voz":
    if st.button("🎤 Escuchar comando"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Escuchando...")
            audio = recognizer.listen(source)
        try:
            texto_ingresado = recognizer.recognize_google(audio, language="es-ES")
            st.success(f"Texto detectado: {texto_ingresado}")
        except Exception as e:
            st.error("No se pudo reconocer el audio.")
            texto_ingresado = ""

# --- Cargar imagen para "reconocimiento facial" ---
st.header("Paso 2: Carga tu imagen para verificación")
imagen_usuario = st.file_uploader("Sube una imagen (jpg, png)", type=["jpg", "png"])

# --- Verificar acceso ---
if st.button("Verificar acceso"):
    if not texto_ingresado:
        st.warning("Primero ingresa o graba un comando.")
    elif not imagen_usuario:
        st.warning("Debes subir una imagen para verificación.")
    else:
        # Validación del texto
        if "abrir la puerta" in texto_ingresado.lower():
            # Cargar imagen autorizada (simulación)
            imagen_autorizada = cv2.imread("autorizados/usuario1.jpg")
            imagen_autorizada = cv2.resize(imagen_autorizada, (200, 200))

            # Cargar imagen del usuario
            imagen_cargada = Image.open(imagen_usuario).convert("RGB")
            imagen_cargada = imagen_cargada.resize((200, 200))
            imagen_np = np.array(imagen_cargada)

            # Simulación simple de "comparación facial"
            diferencia = np.mean(np.abs(imagen_autorizada.astype("float") - imagen_np.astype("float")))

            if diferencia < 50:  # Umbral ajustable
                st.success("✅ Acceso concedido. ¡Puerta abierta!")
                st.image(imagen_cargada, caption="Bienvenido", width=200)
            else:
                st.error("❌ Acceso denegado. No se reconoce el rostro.")
        else:
            st.error("❌ Comando incorrecto. Di 'abrir la puerta'.")
