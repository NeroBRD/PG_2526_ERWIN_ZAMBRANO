## Why

El sistema anterior tenía dos carencias importantes: no proveía información de estado (telemetría) hacia el usuario, y la interfaz web sufría de atascos de red (network queueing) al encolar peticiones HTTP. Adicionalmente, el arranque directo del ESP32 dificultaba la reprogramación al no dejar tiempo para soltar la consola REPL. Esta actualización resuelve la visibilidad de estado en tiempo real, asegura una latencia nula en los controles web, e introduce un menú de inicio robusto para desarrolladores.

## What Changes

- Implementación de telemetría bidireccional: el Arduino Nano ahora reporta su posición de giro y estado cada 500ms al ESP32 por UART.
- El servidor web asíncrono del ESP32 expone un endpoint `/telemetry` para servir estos datos.
- La interfaz web procesa la telemetría para mostrar el estado Online/Offline, el comando actual y la posición del giro.
- Optimización estricta de red (`AbortController` en Javascript) para garantizar que los comandos de parada de emergencia se procesen sin latencia.
- Menú interactivo de 5 segundos en el script de arranque (`boot.py`) para permitir el acceso a la consola de programación antes de que el servidor web tome control.

## Capabilities

### New Capabilities
- `system-boot-process`: Definición del flujo de arranque del ESP32, menú interactivo y timeouts pre-conexión WiFi.

### Modified Capabilities
- `crane-control-logic`: Se añade la generación y transmisión de telemetría desde la lógica central.
- `uart-messaging-protocol`: Se añade el formato de reporte de telemetría unidireccional (Arduino a ESP32).
- `web-server-endpoints`: Se añade el endpoint GET `/telemetry` y la optimización de latencia de red.

## Impact

- `arduino_nano/arduino_nano.ino`: Transmisión activa de telemetría en el puerto Serial.
- `esp32_firmware/main.py`: Tarea asíncrona de lectura de UART, nuevo endpoint JSON y optimizaciones de latencia HTTP.
- `esp32_firmware/index.html`: Nueva interfaz de usuario para telemetría y lógica de máquina de estados para solicitudes Fetch.
- `esp32_firmware/boot.py`: Bloque de interrupción `uselect` introducido antes de la conexión de red.
