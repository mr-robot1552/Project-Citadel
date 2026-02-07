# Room 1 — Motion Detection & Alerting

## Purpose
Room 1 provides first-level intrusion detection using a motion sensor and triggers a local alert to indicate a security breach.

## Hardware Used
- Motion sensor (PIR)
- LED indicator
- Buzzer / speaker
- Raspberry Pi (GPIO)

## Files
- `room1_motion_detection.py` — motion detection + alert logic

## How It Works (High-Level)
- Monitors the motion sensor input on a GPIO pin.
- On detection, activates local indicators (LED/buzzer) to signal a breach.
- Acts as the initial detection layer in Project Citadel’s escalation flow.

## Notes
- Wiring and GPIO mapping are documented in the main project README.
