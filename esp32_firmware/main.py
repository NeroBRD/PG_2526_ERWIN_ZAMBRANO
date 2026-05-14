# main.py
# Este archivo contiene el servidor web asíncrono y la comunicación Serial UART.
import uasyncio as asyncio
from machine import UART, Pin

# ---------------------------------------------------------
# CONFIGURACIÓN DE PINES Y UART
# ---------------------------------------------------------
# Inicializamos el LED integrado para mostrar estado (opcional)
led_status = Pin(2, Pin.OUT)

# Configuración del puerto UART para comunicación con Arduino
# ESP32 TX (GPIO 17) -> Arduino Nano RX (D0)
# Ajustar los pines tx y rx según la necesidad o conexión física real si cambia
uart = UART(2, baudrate=9600, tx=17, rx=16) 

# Variable global para mantener el último comando activo (para evitar spam)
comando_actual = 'S'

# ---------------------------------------------------------
# SERVIDOR WEB
# ---------------------------------------------------------
def leer_html():
    """Lee y retorna el contenido del archivo index.html."""
    try:
        with open('index.html', 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error al cargar index.html: {e}"

async def procesar_peticion(reader, writer):
    """Procesa cada petición HTTP entrante de forma asíncrona."""
    global comando_actual
    
    try:
        # Leemos la primera línea de la petición HTTP (ej: "GET /cmd?c=F HTTP/1.1")
        linea_peticion = await reader.readline()
        linea_peticion = linea_peticion.decode('utf-8').strip()
        
        # Leemos el resto de las cabeceras HTTP y las descartamos (necesario para no atascar el buffer)
        while True:
            header = await reader.readline()
            if header == b'\r\n' or not header:
                break
        
        # Procesamiento básico del enrutamiento
        if "GET / " in linea_peticion:
            # Servir la página web principal
            print("Sirviendo página web...")
            html = leer_html()
            respuesta = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n" + html
            writer.write(respuesta.encode('utf-8'))
            
        elif "GET /cmd?c=" in linea_peticion:
            # Extraer el comando (F, B, U, D, L, R, S)
            comando = linea_peticion.split("GET /cmd?c=")[1].split(" ")[0]
            
            # Enviar el comando por UART al Arduino
            uart.write(comando)
            comando_actual = comando
            print(f"Comando enviado: {comando}")
            
            # Parpadear LED de estado para feedback visual
            led_status.value(1)
            await asyncio.sleep(0.05)
            led_status.value(0)
            
            # Responder OK al cliente (Fetch API)
            respuesta = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nOK"
            writer.write(respuesta.encode('utf-8'))
            
        else:
            # Ruta no encontrada
            respuesta = "HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n"
            writer.write(respuesta.encode('utf-8'))
            
        await writer.drain()
        
    except Exception as e:
        print("Error al procesar la petición:", e)
    finally:
        # Cerrar la conexión
        writer.close()
        await writer.wait_closed()

async def main():
    """Función principal asíncrona que inicia el servidor."""
    print("Iniciando servidor web asíncrono...")
    
    # Encender LED indicando que el servidor está listo
    led_status.value(1)
    
    # Iniciar servidor en el puerto 80
    servidor = await asyncio.start_server(procesar_peticion, "0.0.0.0", 80)
    print("Servidor web escuchando en el puerto 80.")
    
    # Bucle infinito para mantener vivo el servidor
    while True:
        await asyncio.sleep(3600)

# Iniciar el bucle de eventos de uasyncio
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Servidor detenido manualmente.")
