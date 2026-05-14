# Proyecto Grúa Torre - Firmware y Control Web

Este repositorio contiene el código fuente para el sistema de control dual (Manual y Web) de una grúa torre, utilizando un **Arduino Nano** como controlador de motores y un **ESP32** como servidor web y puente de comunicación.

## 🚀 Tecnologías Requeridas

Para compilar, subir y modificar este proyecto, debes tener instalado el siguiente software en tu computadora:

1. **[Arduino IDE (v2.x recomendado)](https://www.arduino.cc/en/software):** Para programar el Arduino Nano en C++.
2. **[Thonny IDE](https://thonny.org/):** Para programar el ESP32 en MicroPython.
3. **[CH340/CP2102 Drivers]:** Si tu Arduino o ESP32 no son reconocidos por la PC, asegúrate de instalar los drivers USB a Serial correspondientes.

### Librerías Necesarias
- **Para Arduino IDE:** Debes instalar la librería `AccelStepper` (Autor: Mike McCauley). Puedes hacerlo desde el Gestor de Librerías de Arduino (`Sketch` -> `Include Library` -> `Manage Libraries...` y buscar `AccelStepper`).

---

## 🛠️ Guía de Despliegue (Cómo instalar el código)

### Paso 1: Configurar el Arduino Nano

1. Abre el programa **Arduino IDE**.
2. Conecta el Arduino Nano a tu computadora mediante un cable USB.
3. Ve a `Herramientas` (`Tools`) y selecciona:
   - **Placa (Board):** `Arduino Nano`
   - **Procesador:** `ATmega328P (Old Bootloader)` (Prueba con el normal si este falla).
   - **Puerto (Port):** Selecciona el puerto COM donde está conectado.
4. Abre el archivo `arduino_nano/arduino_nano.ino` en el IDE.
5. Asegúrate de tener instalada la librería `AccelStepper`.
6. Haz clic en el botón de la flecha hacia la derecha (Subir/Upload). Espera a que diga "Subido" (Done uploading).

### Paso 2: Preparar el ESP32 con MicroPython

1. Abre **Thonny IDE**.
2. Conecta el ESP32 a la computadora vía USB.
3. En Thonny, ve a `Herramientas` -> `Opciones` -> pestaña `Intérprete`.
4. Selecciona **MicroPython (ESP32)** y elige el puerto COM correcto.
5. *Si tu ESP32 es nuevo:* Haz clic en "Install or update MicroPython" en esa misma ventana para flashear el firmware oficial de MicroPython (.bin) en el ESP32.

### Paso 3: Subir el Código al ESP32

1. En **Thonny**, abre los archivos locales ubicados en la carpeta `esp32_firmware` de este proyecto:
   - `boot.py`
   - `main.py`
   - `index.html`
2. Modifica el archivo `boot.py` en tu computadora para colocar las credenciales reales de tu WiFi:
   ```python
   WIFI_SSID = "TU_SSID"
   WIFI_PASSWORD = "TU_PASSWORD"
   ```
3. Guarda estos tres archivos **dentro del dispositivo ESP32** (Thonny te preguntará dónde guardar cuando uses "Guardar como", elige "MicroPython device").
4. Asegúrate de que los archivos se llamen exactamente `boot.py`, `main.py` e `index.html` en la raíz del ESP32.
5. Presiona el botón físico de **Reset/EN** en el ESP32.
6. En la consola de Thonny, verás que se conecta al WiFi y te mostrará la dirección IP (Ejemplo: `192.168.1.50`).

### Paso 4: Pruebas y Uso

1. Realiza las conexiones físicas entre el Arduino y el ESP32 según el documento `requirements.md` (RX del Arduino D0 al TX GPIO17 del ESP32). Es importante conectar ambos GND.
2. Abre un navegador web en tu celular o PC (conectado a la misma red WiFi).
3. Ingresa la dirección IP que te mostró la consola del ESP32.
4. Aparecerá la interfaz de control remoto. ¡Al presionar los botones, el Arduino debería mover los motores correspondientes!

---

## 🔌 Esquema Básico de Pines

**Joysticks (Entradas Arduino):**
- Joystick X (Carro): `A0`
- Joystick Y (Elevación): `A1`
- Joystick Z (Giro): `A2`

**Driver TB6612FNG (Motores DC N20):**
- AIN1: `D2`, AIN2: `D4`, PWMA: `D3` (Carro)
- BIN1: `D7`, BIN2: `D8`, PWMB: `D5` (Elevación)

**Driver DRV8825 (Motor Paso a Paso):**
- STEP: `D9`, DIR: `D10`

**Comunicación:**
- ESP32 TX (`GPIO 17`) ---> Arduino RX (`D0`)
*(Nota: Recuerda desconectar el pin RX del Arduino cuando subas código desde la PC vía USB)*.

---

## 📖 Especificaciones Técnicas (OpenSpec)

La lógica de control, los endpoints del servidor web y el protocolo de mensajería UART están formalmente documentados utilizando el estándar OpenSpec. Puedes encontrar estas especificaciones detalladas en la carpeta de este repositorio:

- **[Lógica de Control](openspec/changes/optimize-crane-code/specs/crane-control-logic/spec.md)**: Prioridades y timeouts de seguridad.
- **[Endpoints Web](openspec/changes/optimize-crane-code/specs/web-server-endpoints/spec.md)**: Rutas HTTP del ESP32.
- **[Protocolo UART](openspec/changes/optimize-crane-code/specs/uart-messaging-protocol/spec.md)**: Comandos seriales.
