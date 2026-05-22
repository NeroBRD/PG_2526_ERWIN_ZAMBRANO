# Delta Spec: Crane Control Logic

## ADDED Requirements

### Requirement: Telemetry reporting
The control loop MUST report the current stepper motor position and the active command via UART.
#### Scenario: Report generation
- Given the system is running
- When 500ms elapse
- Then a report MUST be generated using a non-blocking timer
