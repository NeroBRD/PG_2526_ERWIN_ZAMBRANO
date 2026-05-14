## Why

La implementación actual de la grúa torre cuenta con un sistema de control distribuido (Arduino Nano y ESP32) que se comunican vía UART, además de una interfaz web remota alojada en el ESP32. Para asegurar la mantenibilidad, extensibilidad y claridad del proyecto, es imperativo formalizar el protocolo de comunicación y el funcionamiento del servidor web. Esto estandariza las interacciones y provee una fuente de verdad única sobre las interfaces técnicas del sistema, facilitando futuros desarrollos (como la adición de nuevas funciones de control o clientes).

## What Changes

- Documentación formal de los endpoints HTTP del servidor web asíncrono en el ESP32.
- Definición de la estructura, formatos y temporización del protocolo de mensajería Serial (UART) entre el ESP32 y el Arduino Nano.
- Especificación de las reglas de "timeout" de seguridad (Dead Man's Switch) que gobiernan la parada de emergencia en caso de desconexión.

## Capabilities

### New Capabilities
- `web-server-endpoints`: Especificación de las rutas, parámetros GET/POST y respuestas de la interfaz HTTP del ESP32.
- `uart-messaging-protocol`: Especificación de la comunicación serial entre ESP32 y Arduino, incluyendo mapeo de caracteres a acciones mecánicas (Adelante, Atrás, Giro, etc.).
- `crane-control-logic`: Especificación de las prioridades de control (joystick analógico vs comandos web) y mecanismos de timeout de seguridad.

### Modified Capabilities
- Ninguna.

## Impact

- **Documentación Técnica**: Mejora sustancial en la claridad arquitectónica del proyecto.
- **Implementación Futura**: Cualquier cambio al código en `arduino_nano.ino` o `main.py` deberá adherirse a estos contratos.
- **Interoperabilidad**: Permite que interfaces de terceros (como una aplicación móvil nativa) puedan controlar la grúa adhiriéndose al contrato de los endpoints web y UART.
