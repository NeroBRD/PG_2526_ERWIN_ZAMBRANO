# system-boot-process Specification

## Purpose
TBD - created by archiving change add-telemetry-and-boot-menu. Update Purpose after archive.
## Requirements
### Requirement: Interactive Boot Menu
The ESP32 MUST present a boot menu via the REPL terminal immediately upon starting.
#### Scenario: Menu options
- Given the system boots
- When the terminal is active
- Then it MUST display options to run normally or drop to REPL

### Requirement: Timeout and Execution
The menu MUST time out after exactly 5 seconds.
#### Scenario: Selection handling
- Given the menu is active
- When option 1 is selected or 5s elapses
- Then the system MUST connect to WiFi and execute main
#### Scenario: Developer Mode
- Given the menu is active
- When option 2 is selected
- Then the system MUST exit cleanly to the REPL

