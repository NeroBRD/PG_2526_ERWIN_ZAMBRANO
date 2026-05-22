# boot.py
# Este archivo se ejecuta primero cuando arranca el ESP32.
import network
import time

# ---------------------------------------------------------
# CONFIGURACIÓN DE RED WIFI
# ---------------------------------------------------------
WIFI_SSID = "TU_SSID"        # Reemplazar con el nombre de tu red WiFi
WIFI_PASSWORD = "TU_PASSWORD" # Reemplazar con la contraseña de tu red WiFi

def conectar_wifi():
    """Función robusta para conectar el ESP32 a la red WiFi local."""
    estacion = network.WLAN(network.STA_IF)
    estacion.active(True)
    
    if not estacion.isconnected():
        print("Conectando a la red WiFi...")
        estacion.connect(WIFI_SSID, WIFI_PASSWORD)
        
        # Esperar 10 segundos para la conexión
        intentos = 0
        while not estacion.isconnected() and intentos < 10:
            time.sleep(1)
            intentos += 1
            print(f"Intento {intentos}...")
            
    if estacion.isconnected():
        print("\n¡Conexión WiFi exitosa!")
        print("Configuración de red (IP, Máscara, Puerta de enlace, DNS):")
        print(estacion.ifconfig())
    else:
        print("\nError: No se pudo conectar a la red WiFi. Revisa las credenciales.")

# Ejecutar la conexión al arrancar
conectar_wifi()
