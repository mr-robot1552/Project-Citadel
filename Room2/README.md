# Room 2 — Intruder Trap System

## Purpose
Room 2 simulates an intrusion “trap” that triggers a defensive response when a pressure-based sensor is activated.

## Hardware Used
- Force Sensitive Resistor (FSR)
- ADC (analog-to-digital conversion)
- Relay module
- Water pump
- Raspberry Pi (GPIO)

## Files
- `room2_intruder_trap.py` — sensor trigger + relay/pump control + authorization flow

## How It Works (High-Level)
- Reads the pressure sensor through the ADC.
- Detects a threshold event indicating a step/pressure trigger.
- Activates the relay-controlled pump to simulate containment/asset denial.
- Includes an authorization step to arm/disarm the response.

## Notes
- Wiring and GPIO mapping are documented in the main project README.
