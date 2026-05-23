# boot.py
# Este archivo se ejecuta primero cuando arranca el ESP32.
import network
import time
import sys
import uselect

# ---------------------------------------------------------
# CONFIGURACIÓN DE RED WIFI Y VERSIÓN
# ---------------------------------------------------------
FIRMWARE_VERSION = "1.2.0-PRO"
WIFI_SSID = "TU_SSID"        # Reemplazar con el nombre de tu red WiFi
WIFI_PASSWORD = "TU_PASSWORD" # Reemplazar con la contraseña de tu red WiFi

def conectar_wifi():
    """Función robusta para conectar el ESP32 a la red WiFi local."""
    estacion = network.WLAN(network.STA_IF)
    
    # Forzar un reseteo del módulo WiFi para evitar "Wifi Internal State Error" tras un soft reboot
    estacion.active(False)
    time.sleep(0.5)
    estacion.active(True)
    estacion.disconnect()
    
    if not estacion.isconnected():
        print("Conectando a la red WiFi...")
        estacion.connect(WIFI_SSID, WIFI_PASSWORD)
        
        # Esperar hasta 10 segundos para la conexión
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

def menu_inicio(timeout_segundos=5):
    """
    Muestra un menú en la terminal. Avanza automáticamente si no hay respuesta.
    """
    print("\n" + "="*45)
    print(f"  SISTEMA DE CONTROL - GRÚA TORRE v{FIRMWARE_VERSION}")
    print("="*45)
    print("1. Iniciar sistema normalmente (Modo Ejecución)")
    print("2. Detener en modo programación (Liberar REPL)")
    print(f"Selecciona una opción (Avanza a opción 1 en {timeout_segundos}s)...")
    
    # Configurar la terminal para escuchar la entrada del usuario sin bloquear
    poller = uselect.poll()
    poller.register(sys.stdin, uselect.POLLIN)
    
    tiempo_inicio = time.time()
    while (time.time() - tiempo_inicio) < timeout_segundos:
        # Revisar si hay datos en la terminal (espera hasta 100ms por ciclo)
        if poller.poll(100):
            caracter = sys.stdin.read(1)
            if caracter == '1':
                print("\n-> Opción 1 seleccionada. Iniciando...")
                return True
            elif caracter == '2':
                print("\n-> Opción 2 seleccionada. Modo programación activo.")
                print("Consola REPL liberada. Puedes subir o modificar archivos.")
                return False
    
    # Si se agota el tiempo sin respuesta, asumimos que está corriendo en la grúa de forma autónoma
    print("\n-> Tiempo de espera agotado. Iniciando de forma automática...")
    return True

# --- FLUJO DE INICIO ---

# Ejecutamos el menú ANTES de conectar al WiFi o cargar el main
if menu_inicio(timeout_segundos=5):
    # Si elige 1 o se agota el tiempo, conecta a WiFi y avanza a main.py
    conectar_wifi()
else:
    # Si elige 2, forzamos la detención del script del sistema operativo
    # Esto evita que MicroPython salte automáticamente a ejecutar el main.py
    sys.exit()
