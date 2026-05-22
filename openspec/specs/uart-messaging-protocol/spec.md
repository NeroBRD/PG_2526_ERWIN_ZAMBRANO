# uart-messaging-protocol Specification

## Purpose
TBD - created by archiving change optimize-crane-code. Update Purpose after archive.
## Requirements
### Requirement: Baud Rate y Conexión
La comunicación serial UART entre ESP32 (TX GPIO 17) y Arduino Nano (RX D0) MUST establecerse a 9600 baudios.

#### Scenario: Transmisión de datos
- **WHEN** el ESP32 inicializa el puerto UART
- **THEN** lo hace con velocidad de 9600 baudios, 8 bits de datos, sin paridad y 1 bit de parada (8N1)

### Requirement: Conjunto de Comandos
El protocolo UART MUST utilizar un único carácter ASCII en mayúsculas por comando para instruir el movimiento.

#### Scenario: Movimiento del Carro
- **WHEN** el Arduino Nano recibe `F`
- **THEN** activa el motor del carro hacia adelante
- **WHEN** el Arduino Nano recibe `B`
- **THEN** activa el motor del carro hacia atrás

#### Scenario: Movimiento de Elevación
- **WHEN** el Arduino Nano recibe `U`
- **THEN** activa el motor de elevación para subir el gancho
- **WHEN** el Arduino Nano recibe `D`
- **THEN** activa el motor de elevación para bajar el gancho

#### Scenario: Movimiento de Giro
- **WHEN** el Arduino Nano recibe `L`
- **THEN** activa el motor paso a paso para girar a la izquierda
- **WHEN** el Arduino Nano recibe `R`
- **THEN** activa el motor paso a paso para girar a la derecha

#### Scenario: Comando de Parada
- **WHEN** el Arduino Nano recibe `S`
- **THEN** detiene todos los motores activos accionados remotamente

### Requirement: Telemetry Format
The Arduino MUST transmit telemetry strings to the ESP32 in the format `T:<pos>,<cmd>\n`.
#### Scenario: Transmission formatting
- Given telemetry data is ready
- When it is transmitted
- Then it MUST follow the `T:<pos>,<cmd>\n` pattern

### Requirement: Non-blocking reception
The ESP32 MUST implement a non-blocking mechanism to read incoming UART telemetry strings.
#### Scenario: Error handling
- Given a malformed string
- When the ESP32 reads it
- Then it MUST discard it silently

