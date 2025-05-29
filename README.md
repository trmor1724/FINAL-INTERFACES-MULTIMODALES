# cerradura_gestos

# Cerradura Inteligente con Reconocimiento de Imágenes 🔒📸

## Descripción
Sistema de cerradura inteligente que utiliza reconocimiento de imágenes mediante IA para controlar el acceso. La aplicación está desarrollada con Streamlit e integra un modelo de Keras para el reconocimiento de gestos, comunicándose mediante MQTT para el control de la cerradura.

## Características Principales
- 📸 Captura de imágenes en tiempo real
- 🤖 Reconocimiento de gestos mediante IA
- 🌐 Comunicación MQTT
- 🔐 Control de cerradura (abrir/cerrar)
- 📊 Interfaz web interactiva

## Requisitos Previos
```
- Python 3.7+
- Streamlit
- OpenCV
- Keras
- Paho-MQTT
- Pillow
- NumPy
- Modelo entrenado (keras_model.h5)
```

## Instalación
1. Clona el repositorio
2. Instala las dependencias:
```bash
pip install streamlit opencv-python keras paho-mqtt pillow numpy
```
3. Asegúrate de tener el modelo `keras_model.h5` en el directorio del proyecto

## Configuración MQTT
- Broker: broker.hivemq.com
- Puerto: 1883
- Cliente ID: APP_CERR
- Tópico de publicación: "IMIA"

## Uso
1. Inicia la aplicación:
```bash
streamlit run app.py
```

2. Interfaz de Usuario:
   - Accede a la cámara web
   - Captura una imagen
   - El sistema reconocerá automáticamente el gesto
   - La cerradura responderá según el gesto detectado

3. Gestos Reconocidos:
   - Gesto de apertura (predicción[0][0] > 0.3)
   - Gesto de cierre (predicción[0][1] > 0.3)

## Estructura del Código

### Importaciones Principales
```python
import paho.mqtt.client as paho
import streamlit as st
import cv2
import numpy as np
from PIL import Image
from keras.models import load_model
```

### Componentes Clave

1. **Configuración MQTT**
```python
def on_publish(client, userdata, result):
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)
```

2. **Procesamiento de Imágenes**
- Captura mediante Streamlit
- Redimensionamiento a 224x224 píxeles
- Normalización de datos
- Predicción mediante modelo Keras

3. **Control de Cerradura**
- Publicación de comandos vía MQTT
- Estados: 'Abre' y 'Cierra'
- Formato JSON para mensajes

## Flujo de Trabajo
1. Inicialización:
   - Conexión al broker MQTT
   - Carga del modelo Keras
   - Configuración de la interfaz Streamlit

2. Captura y Procesamiento:
   - Captura de imagen vía webcam
   - Preprocesamiento y normalización
   - Inferencia mediante modelo IA

3. Control:
   - Interpretación de predicciones
   - Envío de comandos MQTT
   - Actualización de interfaz

## Personalización del Modelo
El sistema utiliza un modelo Keras preentrenado:
- Entrada: Imágenes 224x224x3
- Salida: 2 clases (abrir/cerrar)
- Umbral de confianza: 0.3

## Seguridad
- Comunicación MQTT no encriptada (considerar implementar TLS)
- Validación de gestos mediante umbral de confianza
- Sin almacenamiento permanente de imágenes

## Limitaciones
- Requiere conexión a internet
- Depende de la calidad de la cámara
- Latencia según conexión MQTT
- Necesita buena iluminación

## Troubleshooting
1. Problemas de conexión MQTT:
   - Verificar conectividad
   - Comprobar broker y puerto
   - Revisar permisos de firewall

2. Problemas de cámara:
   - Verificar permisos del navegador
   - Comprobar dispositivo de captura
   - Asegurar iluminación adecuada

## Desarrollo Futuro
- Implementar cifrado TLS
- Agregar autenticación
- Mejorar modelo de IA
- Añadir registro de accesos
- Implementar modo nocturno

## Contribuciones
Se aceptan contribuciones mediante Pull Requests:
1. Fork del repositorio
2. Crear rama de características
3. Commit de cambios
4. Push a la rama
5. Crear Pull Request

## Licencia
[Especificar tipo de licencia]

## Créditos
- Desarrollado con Streamlit
- Modelo IA: Keras
- Comunicación: HiveMQ
