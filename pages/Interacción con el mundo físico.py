import streamlit as st
import serial
import serial.tools.list_ports
import time
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Monitor de Distancia Arduino", layout="wide")

# Título de la aplicación
st.title("Sistema de Monitoreo Ultrasónico con Arduino")

# Función para detectar puertos seriales disponibles
def detect_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

# Sidebar para configuración
with st.sidebar:
    st.header("Configuración de Conexión")
    
    # Selección de puerto
    available_ports = detect_ports()
    selected_port = st.selectbox("Seleccionar Puerto COM", available_ports)
    
    # Botón de conexión
    connect_button = st.button("Conectar a Arduino")
    disconnect_button = st.button("Desconectar")
    
    # Configuración de alertas
    st.header("Configuración de Alertas")
    threshold_distance = st.slider("Distancia de alerta (cm)", 0, 200, 50)
    alert_tone = st.selectbox("Tono de alerta", [262, 294, 330, 349, 392, 440, 494])
    
    # Opciones de visualización
    st.header("Opciones de Visualización")
    sample_rate = st.slider("Tasa de muestreo (ms)", 100, 2000, 500)

# Estado de la conexión
if 'connected' not in st.session_state:
    st.session_state.connected = False
if 'serial_conn' not in st.session_state:
    st.session_state.serial_conn = None
if 'data' not in st.session_state:
    st.session_state.data = []

# Manejo de conexión
if connect_button and not st.session_state.connected:
    try:
        st.session_state.serial_conn = serial.Serial(selected_port, 9600, timeout=1)
        time.sleep(2)  # Esperar a que se establezca la conexión
        st.session_state.connected = True
        st.sidebar.success("Conectado al Arduino!")
    except Exception as e:
        st.sidebar.error(f"Error de conexión: {e}")

if disconnect_button and st.session_state.connected:
    st.session_state.serial_conn.close()
    st.session_state.connected = False
    st.sidebar.info("Desconectado del Arduino")

# Contenedores para la visualización
status_container = st.container()
chart_container = st.container()
data_container = st.container()

# Bucle principal de la aplicación
while True:
    with status_container:
        st.subheader("Estado del Sistema")
        
        # Columnas para métricas
        col1, col2, col3 = st.columns(3)
        
        if st.session_state.connected:
            try:
                # Leer datos del Arduino
                if st.session_state.serial_conn.in_waiting > 0:
                    line = st.session_state.serial_conn.readline().decode('utf-8').strip()
                    
                    try:
                        current_distance = float(line)
                        
                        # Actualizar métricas
                        with col1:
                            st.metric("Distancia Actual", f"{current_distance:.2f} cm")
                        
                        with col2:
                            status = "ALERTA" if current_distance < threshold_distance else "Normal"
                            st.metric("Estado", status, delta=None, delta_color="inverse")
                        
                        with col3:
                            st.metric("Umbral de Alerta", f"{threshold_distance} cm")
                        
                        # Guardar datos para el gráfico
                        timestamp = pd.Timestamp.now()
                        st.session_state.data.append({
                            "timestamp": timestamp,
                            "distance": current_distance,
                            "status": status
                        })
                        
                        # Mantener solo los últimos 100 puntos
                        if len(st.session_state.data) > 100:
                            st.session_state.data.pop(0)
                        
                        # Enviar comandos al Arduino si es necesario
                        if current_distance < threshold_distance:
                            command = f"ALERT,{alert_tone}\n"
                            st.session_state.serial_conn.write(command.encode())
                        else:
                            st.session_state.serial_conn.write(b"NORMAL\n")
                        
                    except ValueError:
                        pass
                
            except Exception as e:
                st.error(f"Error de comunicación: {e}")
                st.session_state.connected = False
        else:
            col1.metric("Distancia Actual", "N/A")
            col2.metric("Estado", "Desconectado")
            col3.metric("Umbral de Alerta", f"{threshold_distance} cm")
    
    # Mostrar gráfico con los datos históricos
    with chart_container:
        st.subheader("Gráfico de Distancia en Tiempo Real")
        if st.session_state.data:
            df = pd.DataFrame(st.session_state.data)
            fig = px.line(df, x="timestamp", y="distance", 
                          title="Distancia medida por el sensor ultrasónico",
                          labels={"distance": "Distancia (cm)", "timestamp": "Tiempo"},
                          color="status",
                          color_discrete_map={"ALERTA": "red", "Normal": "green"})
            fig.add_hline(y=threshold_distance, line_dash="dash", line_color="orange",
                         annotation_text=f"Umbral: {threshold_distance} cm")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Esperando datos... Conecta el Arduino para comenzar.")
    
    # Mostrar tabla de datos
    with data_container:
        st.subheader("Datos Recientes")
        if st.session_state.data:
            df = pd.DataFrame(st.session_state.data)
            st.dataframe(df.tail(10), use_container_width=True)
        else:
            st.info("No hay datos disponibles")
    
    # Controlar la tasa de actualización
    time.sleep(sample_rate / 1000)
