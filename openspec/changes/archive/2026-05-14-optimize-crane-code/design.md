## Context

El sistema de la Grúa Torre utiliza dos controladores principales (Arduino Nano y ESP32) para gestionar operaciones manuales vía joystick y operaciones remotas vía web. Actualmente, el código está implementado, pero requiere una especificación estricta de sus interfaces (endpoints y protocolo UART) para asegurar robustez, depuración estructurada y permitir futuras integraciones.

## Goals / Non-Goals

**Goals:**
- Definir el contrato de comunicación serial (UART) entre el ESP32 y el Arduino Nano.
- Especificar los endpoints HTTP expuestos por el servidor web del ESP32.
- Establecer las prioridades de control (web vs joystick) y los tiempos de seguridad.

**Non-Goals:**
- Refactorizar el código existente en `arduino_nano.ino` o `main.py` (esta tarea es estrictamente de documentación).
- Cambiar la arquitectura de hardware o los componentes físicos de la grúa.

## Decisions

- **Protocolo UART basado en Caracteres (ASCII):** Se decide documentar el uso de caracteres individuales (`F`, `B`, `U`, `D`, `L`, `R`, `S`) en lugar de tramas JSON o strings complejas. *Razón:* Optimización del ancho de banda y menor sobrecarga computacional en el Arduino Nano.
- **Polling Constante vs Eventos (Timeout):** El servidor enviará continuamente el comando web cada 200ms mientras el usuario mantenga el botón. El Arduino implementará un timeout de 500ms; si no recibe ningún carácter en ese lapso, asumirá una desconexión y detendrá motores. *Razón:* Prevenir que la grúa continúe moviéndose si la conexión WiFi se corta repentinamente.
- **RESTful Endpoints vs WebSockets:** Se utiliza HTTP GET simple con parámetros en la query string (`/cmd?c=X`) en lugar de WebSockets. *Razón:* Menor complejidad para implementar el cliente y suficiente reactividad para esta aplicación (vía Fetch API).

## Risks / Trade-offs

- **[Riesgo] Colisión de Comandos (Web vs Joystick):** Si un usuario acciona el joystick y otro usuario envía comandos por la web simultáneamente.
  - **Mitigación:** La especificación detallará que los comandos web sobrescriben la intención del joystick para prevenir movimientos erráticos y asegurar un control absoluto del sistema de emergencia si fuera necesario.
- **[Trade-off] Falta de acuse de recibo (ACK) en UART:** El ESP32 envía el carácter pero el Arduino no responde confirmando.
  - **Mitigación:** Aceptable dada la simplicidad del sistema. La retroalimentación visual la recibe el operador remoto directamente observando la grúa.
