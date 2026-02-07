# Radar System — Real-Time Detection & Visualization

## Purpose
The Radar System provides real-time distance scanning and visualization to extend situational awareness beyond the room-level sensors. It combines a Raspberry Pi controller (sensor + servo sweep) with a Processing-based GUI for live radar-style display.

## Hardware Used
- Ultrasonic sensor (HC-SR04)
- Servo motor (sweep control)
- Raspberry Pi (GPIO)

## Files
- `radar_controller.py` — controls the ultrasonic sensor + servo sweep and streams angle/distance readings over TCP
- `radar_gui.pde` — Processing GUI that connects over TCP and renders a radar visualization

## How It Works (High-Level)
- The Raspberry Pi sweeps the ultrasonic sensor using a servo motor across an angle range.
- For each angle step, distance is measured and transmitted as a TCP data stream in the format: `angle,distance`.
- The Processing GUI connects to the Raspberry Pi TCP server, reads the stream, and renders a radar-style sweep with detected distance points.
- This subsystem demonstrates real-time sensing + visualization within the Project Citadel architecture.

## Run Notes
- The radar controller runs on the Raspberry Pi and listens for a TCP client connection (default port: `5005`).
- The GUI runs in Processing on a computer and connects to the controller using the configured host/port in `radar_gui.pde`.
- This repository reflects the final academic implementation; physical hardware is required to execute and validate runtime behavior.

## Media
See the `/media` folder for diagrams and visuals used in the project documentation.
