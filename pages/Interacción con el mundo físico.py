import streamlit as st
from streamlit_autorefresh import st_autorefresh
import paho.mqtt.client as mqtt

st.set_page_config(page_title="🛰️ Monitor PIR - Casa Inteligente", layout="centered")
st.title("📡 Movimiento en tiempo real (desde Wokwi)")

# Estado global para el último mensaje
if "movimiento" not in st.session_state:
    st.session_state.movimiento = "Esperando datos..."

# Callback cuando se recibe mensaje MQTT
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    st.session_state.movimiento = f"📍 Movimiento: **{payload}**"

# Configurar cliente MQTT
client = mqtt.Client()
client.on_message = on_message
client.connect("broker.mqttdashboard.com", 1883, 60)
client.subscribe("casa/movimiento")
client.loop_start()

# Refrescar cada 2 segundos
st_autorefresh(interval=2000, key="datarefresh")

# Mostrar el estado actual
st.markdown(st.session_state.movimiento)
