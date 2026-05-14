# crane-control-logic Specification

## Purpose
TBD - created by archiving change optimize-crane-code. Update Purpose after archive.
## Requirements
### Requirement: Prioridad de Control
El sistema MUST priorizar las señales recibidas vía remota (web/UART) sobre las señales analógicas locales (Joysticks) para garantizar una parada de emergencia y control override efectivos.

#### Scenario: Comando web durante uso de joystick
- **WHEN** el operador local mueve el joystick del carro hacia adelante
- **AND** el operador remoto envía el comando `B` (atrás) vía web
- **THEN** el Arduino Nano ignora la entrada analógica y mueve el carro hacia atrás según el comando serial

### Requirement: Timeout de Seguridad (Dead Man's Switch)
El Arduino Nano MUST detener cualquier movimiento instanciado de forma remota si no recibe un nuevo comando web en un plazo máximo establecido.

#### Scenario: Pérdida de conexión web
- **WHEN** el Arduino Nano recibe un comando de movimiento continuo (ej: `F`)
- **AND** transcurren 500 ms sin recibir ningún nuevo carácter por el puerto Serial
- **THEN** el Arduino Nano asume la desconexión del cliente web, establece el comando actual a `S` (Stop) y detiene los motores afectados

### Requirement: Envío Continuo desde Interfaz Gráfica
Para mantener viva la orden de movimiento, la interfaz web del ESP32 MUST enviar la orden repetidamente mientras el usuario mantenga pulsado el botón.

#### Scenario: Mantener botón pulsado en la web
- **WHEN** el usuario mantiene presionado el botón "Adelante"
- **THEN** la interfaz web envía la petición GET `/cmd?c=F` cada 200 ms de forma ininterrumpida
- **WHEN** el usuario suelta el botón "Adelante"
- **THEN** la interfaz web envía inmediatamente la petición GET `/cmd?c=S` una única vez

