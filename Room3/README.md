# Room 3 — Gas Release Simulation

## Purpose
Room 3 simulates a gas-release event triggered by a perimeter breach and provides a visible on-device alert.

## Hardware Used
- Laser + LDR (tripwire breach detection)
- LCD1602 I2C display
- Ultrasonic humidifier
- Raspberry Pi (GPIO)

## Files
- `room3_gas_release_sim.py` — tripwire detection + humidifier control + LCD messaging

## How It Works (High-Level)
- Monitors the LDR to detect laser interruption (breach).
- On breach, activates the humidifier to simulate gas release.
- Displays an alert on the LCD and requires a deactivation keyword to reset.

## Notes
- Wiring and GPIO mapping are documented in the main project README.
