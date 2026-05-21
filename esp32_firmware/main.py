# main.py
# Este archivo contiene el servidor web asíncrono y la comunicación Serial UART.
import uasyncio as asyncio
from machine import UART, Pin
import json
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
# Variable global para almacenar el estado de la telemetría
estado_grua = {"pos": 0, "cmd": "S"}
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
async def leer_uart():
    """Lee constantemente los datos de telemetría enviados por el Arduino."""
    sreader = asyncio.StreamReader(uart)
    while True:
        try:
            linea = await sreader.readline()
            if linea:
                texto = linea.decode('utf-8').strip()
                if texto.startswith("T:"):
                    # Ejemplo: "T:1500,F"
                    datos = texto[2:].split(',')
                    if len(datos) == 2:
                        estado_grua["pos"] = int(datos[0])
                        estado_grua["cmd"] = datos[1]
                        # Mostrar la telemetría recibida en la consola de Thonny
                        print(f"[Telemetría] Posición Giro: {estado_grua['pos']} | Comando Activo: {estado_grua['cmd']}")
        except Exception as e:
            print("Error leyendo UART:", e)
        await asyncio.sleep(0.05)
async def apagar_led():
    await asyncio.sleep(0.05)
    led_status.value(0)
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
            
            # Parpadear LED de estado sin bloquear la respuesta
            led_status.value(1)
            asyncio.create_task(apagar_led())
            
            # Responder OK al cliente (Fetch API) inmediatamente
            respuesta = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nOK"
            writer.write(respuesta.encode('utf-8'))
            
        elif "GET /telemetry " in linea_peticion:
            # Enviar el estado actual de la telemetría como JSON
            datos_json = json.dumps(estado_grua)
            respuesta = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nConnection: close\r\n\r\n" + datos_json
            writer.write(respuesta.encode('utf-8'))
            
        else:
            # Ruta no encontrada
            respuesta = "HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n"
            writer.write(respuesta.encode('utf-8'))
            
        await writer.drain()
        
    except OSError as e:
        # 104 = ECONNRESET, 103 = ECONNABORTED, 32 = EPIPE
        if len(e.args) > 0 and e.args[0] in (104, 103, 32):
            # El navegador cerró la conexión a propósito (AbortController funcionó)
            pass
        else:
            print("Error de red (OSError) al procesar petición:", e)
    except Exception as e:
        print("Error general al procesar la petición:", e)
    finally:
        # Cerrar la conexión
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass
async def main():
    """Función principal asíncrona que inicia el servidor."""
    print("Iniciando servidor web asíncrono...")
    
    # Encender LED indicando que el servidor está listo
    led_status.value(1)
    
    # Iniciar tarea asíncrona de lectura de telemetría UART
    asyncio.create_task(leer_uart())
    
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