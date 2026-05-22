# Delta Spec: UART Messaging Protocol

## ADDED Requirements

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
