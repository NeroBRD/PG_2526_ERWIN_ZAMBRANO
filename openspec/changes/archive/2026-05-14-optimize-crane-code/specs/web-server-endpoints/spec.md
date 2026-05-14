## ADDED Requirements

### Requirement: Endpoints de Movimiento
El servidor web asíncrono del ESP32 MUST exponer un endpoint `/cmd` que procese peticiones GET para despachar comandos a la grúa.

#### Scenario: Comando válido
- **WHEN** el cliente hace una petición HTTP GET a `/cmd?c=F`
- **THEN** el ESP32 transmite el carácter `F` vía UART y responde HTTP 200 OK

#### Scenario: Comando inválido o ausente
- **WHEN** el cliente hace una petición HTTP GET a `/cmd` sin parámetro `c`
- **THEN** el ESP32 no transmite datos por UART y responde HTTP 404 (o lo maneja silenciando)

### Requirement: Endpoint de Interfaz Gráfica
El servidor web MUST exponer la ruta raíz `/` para servir el archivo `index.html`.

#### Scenario: Solicitud de página principal
- **WHEN** el cliente accede mediante GET a `/`
- **THEN** el ESP32 responde con HTTP 200 OK y el contenido de la interfaz web
