import paho.mqtt.client as paho
import time
import json
import streamlit as st
import cv2
import numpy as np
from PIL import Image
from keras.models import load_model

# Configuración del cliente MQTT
def on_publish(client, userdata, result):
    print("✅ Dato publicado al broker MQTT")
    pass

def on_message(client, userdata, message):
    global message_received
    message_received = str(message.payload.decode("utf-8"))
    st.write("📩 Mensaje recibido:", message_received)

# Configurar broker MQTT
broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("cerradura-inteligente")
client1.on_message = on_message
client1.on_publish = on_publish
client1.connect(broker, port)

# Cargar modelo
model = load_model("keras_model.h5")

# Configuración de Streamlit
st.set_page_config(page_title="Cerradura Inteligente", layout="centered")
st.title("🔐 Cerradura Inteligente con Streamlit + Keras + MQTT")
st.write("Toma una foto y el modelo decidirá si debe abrir o cerrar la puerta.")

# Captura de imagen desde cámara
img_file_buffer = st.camera_input("📷 Toma una foto")

if img_file_buffer is not None:
    # Leer imagen
    img = Image.open(img_file_buffer).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img)

    # Normalizar
    normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array

    # Predicción
    prediction = model.predict(data)
    st.write("📊 Predicción:", prediction)

    # Clasificación
    if prediction[0][0] > 0.3:
        st.success("✅ Abriendo la puerta")
        client1.publish("GOYO", json.dumps({"gesto": "Abre"}), qos=0, retain=False)
    elif prediction[0][1] > 0.3:
        st.warning("🔒 Cerrando la puerta")
        client1.publish("GOYO", json.dumps({"gesto": "Cierra"}), qos=0, retain=False)
    else:
        st.error("❌ Gesto no reconocido")
t
