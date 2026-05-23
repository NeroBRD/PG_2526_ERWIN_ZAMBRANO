# Design: Advanced UI Features

## Architecture

Since memory on the ESP32 is highly constrained, all advanced logic will run entirely on the client side (browser). 
The ESP32 server will be upgraded to use chunked streaming (512 bytes) to serve the enlarged `index.html` without triggering `MemoryError`.

### 1. Theme and Layout Engine
- **CSS Variables**: A `:root` scope and `[data-theme]` attributes will manage color tokens.
- **Persistence**: `localStorage.setItem` and `getItem` will be used to restore the theme and the order of the control panels (`ordenPaneles` array).

### 2. Macro State Machine
- **State Variables**: `grabandoMacro`, `reproduciendoMacro`, and a `macroSecuencia` array of `{ cmd, t }` objects.
- **Execution**: An async function using `await new Promise(r => setTimeout(r, delay))` will ensure timing accuracy between recorded commands.

### 3. Gyroscope Controller
- **Sensor**: `window.addEventListener('deviceorientation')`
- **Mapping**: 
  - `beta` (pitch): Maps to Carro (Adelante/Atras)
  - `gamma` (roll): Maps to Giro (Izq/Der)
- **Deadzone**: A threshold of 20 degrees will be implemented to ignore hand tremors.
- **Security Bypass**: Because modern browsers block sensors on HTTP, a visible debug div will warn the user to enable `Insecure origins treated as secure` in `chrome://flags`.
