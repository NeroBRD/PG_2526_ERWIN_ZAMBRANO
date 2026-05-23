# web-interface-features Specification

## Purpose
TBD - created by archiving change advanced-ui-features. Update Purpose after archive.
## Requirements
### Requirement: Theming and Layout Memory
The web interface MUST allow users to switch themes and reorder control panels, persisting these choices across sessions.
#### Scenario: Theme switching
- Given the web interface is loaded
- When the user selects a theme
- Then it MUST be saved to localStorage and applied immediately

### Requirement: Macro Recording
The web interface MUST provide a mechanism to record a sequence of commands with their exact timestamps.
#### Scenario: Routine playback
- Given a recorded macro sequence
- When the user presses Play
- Then the browser MUST dispatch the exact fetch requests with the recorded millisecond delays

### Requirement: Immersive Gyroscope Control
The web interface MUST read `beta` and `gamma` orientation data to dispatch movement commands.
#### Scenario: Pitch control
- Given the immersive mode is active
- When the phone pitches forward past 20 degrees
- Then the Carro 'B' command MUST be dispatched

