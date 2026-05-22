# web-server-endpoints Specification

## Purpose
TBD - created by archiving change optimize-crane-code. Update Purpose after archive.
## Requirements
### Requirement: Endpoints de Movimiento
El servidor web asíncrono del ESP32 MUST exponer un endpoint `/cmd` que procese peticiones GET para despachar comandos a la grúa sin retrasos artificiales bloqueantes.
#### Scenario: Comando válido sin latencia
- **WHEN** el cliente hace una petición HTTP GET a `/cmd?c=F`
- **THEN** el ESP32 transmite el carácter `F` vía UART y responde HTTP 200 OK inmediatamente sin esperar al parpadeo del LED.

### Requirement: Endpoint de Interfaz Gráfica
El servidor web MUST exponer la ruta raíz `/` para servir el archivo `index.html`.

#### Scenario: Solicitud de página principal
- **WHEN** el cliente accede mediante GET a `/`
- **THEN** el ESP32 responde con HTTP 200 OK y el contenido de la interfaz web

### Requirement: Telemetry API
The server MUST expose a `GET /telemetry` endpoint returning a JSON object.
#### Scenario: Payload validation
- Given a request to `/telemetry`
- When the server responds
- Then the JSON object MUST contain `pos` and `cmd` keys.

### Requirement: Client polling
The web interface MUST poll `/telemetry` at 500ms intervals.
#### Scenario: Network abortion
- Given a pending fetch request
- When a Stop command is issued
- Then the pending request MUST be aborted immediately

