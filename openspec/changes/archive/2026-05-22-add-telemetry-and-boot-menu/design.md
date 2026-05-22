# Design: add-telemetry-and-boot-menu

## Architecture
- El sistema adopta un enfoque asíncrono no bloqueante en ambos microcontroladores.
- La interfaz de usuario implementa una máquina de estados estricta para peticiones de red (evitando encolamientos).

## Components
- **Boot Menu (`boot.py`)**: Un bucle `uselect.poll()` intercepta la entrada estándar por 5 segundos antes de ceder el control.
- **ESP32 Telemetry Reader**: Un bucle asíncrono lee `UART.readline()` sin bloquear el servidor HTTP.
- **Web UI Engine**: Las peticiones `fetch()` se encapsulan en instancias de `AbortController` para cancelar consultas estancadas instantáneamente.

## Data Structures
- Carga útil de Telemetría (UART): `T:<posición>,<comando>\n`
- Carga útil de JSON (HTTP): `{"pos": 0, "cmd": "S"}`
