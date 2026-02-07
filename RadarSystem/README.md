# Radar System — Real-Time Detection & Visualization

## Purpose
The Radar System provides real-time distance scanning and visualization to extend situational awareness beyond the room-level sensors. It combines a Raspberry Pi controller (sensor + servo sweep) with a Processing-based GUI for live radar-style display.

## Hardware Used
- Ultrasonic sensor (HC-SR04)
- Servo motor (sweep control)
- Raspberry Pi (GPIO)

## Files
- `radar_controller.py` — controls the ultrasonic sensor + servo sweep and outputs live distance readings
- `radar_gui.pde` — Processing GUI that reads the live distance stream and renders radar visualization

## How It Works (High-Level)
- The Raspberry Pi sweeps the ultrasonic sensor using a servo motor across an angle range.
- For each angle step, distance is measured and formatted as a live data stream.
- The Processing GUI receives the stream and renders a radar-style sweep with detected distance points.
- This subsystem is designed to demonstrate real-time sensor fusion + visualization as part of the Project Citadel architecture.

## Run Notes
- Run `radar_controller.py` on the Raspberry Pi.
- Run `radar_gui.pde` on a computer with Processing installed.
- Ensure both sides are configured to communicate using the same method defined in the code (serial or network).
- Wiring and GPIO mapping are documented in the main project README.

## Media
See the `/media` folder for diagrams and visuals used in the project documentation.
