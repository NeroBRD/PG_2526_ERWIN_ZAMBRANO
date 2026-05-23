# Proposal: Advanced UI Features (Themes, Macros, Gyroscope)

## Problem
The current tower crane remote control web interface is purely functional but lacks modern convenience and presentation features. Specifically, the visual theme is hardcoded, the layout cannot be customized for left/right-handed users, repetitive testing routines must be run manually, and there is no immersive presentation mode (e.g., using physical sensors).

## Proposed Solution
We propose overhauling `index.html` to introduce an advanced, client-side only Javascript architecture that provides:
1. **CSS Theming**: Three persistent visual themes (Industrial, Neon, Day).
2. **Modular Layout**: Reorderable control panels saved to `localStorage`.
3. **Macro Engine**: A state machine capable of recording and precisely repeating control sequences.
4. **Immersive Gyroscope Mode**: Leveraging the `DeviceOrientationEvent` to translate physical phone tilt into X/Y axis control commands for the crane.

## Goals
- Provide a premium user experience.
- Implement complex features without modifying the ESP32 server Python code.
- Provide fallback mechanisms and debug info for browser sensor security limitations.
