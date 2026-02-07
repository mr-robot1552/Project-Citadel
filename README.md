# Project Citadel – Nineveh Shadow Ops Facility

## Project Overview
Project Citadel – Nineveh Shadow Ops Facility is a multi-room, layered security system developed as an academic capstone project for the Computer Engineering Technology program. The system is designed to demonstrate progressive intrusion detection and deterrence using a centralized Raspberry Pi controller, distributed sensors, and modular countermeasures.

The project implements escalating security responses across three distinct rooms, each representing a higher security level. Optional subsystems, including real-time surveillance and an ultrasonic radar with TCP/IP visualization, extend situational awareness beyond the internal security perimeter. The system emphasizes modularity, scalability, and clear separation between detection, response, and monitoring components.

---

## System Architecture
The system is centrally managed by a Raspberry Pi 4, which coordinates all sensor inputs, authorization logic, and countermeasure outputs. Each room operates as an independent security module while remaining integrated into the overall system architecture.

Security escalation is implemented as follows:
- Room 1 provides initial detection and alerting
- Room 2 introduces physical countermeasures to protect sensitive materials
- Room 3 deploys advanced deterrents for high-security areas

Optional subsystems, such as surveillance cameras and an external radar system, operate alongside the core room architecture without requiring changes to existing logic, reinforcing the system’s modular design.

---

## Functional Breakdown

### Room 1 – Motion Detection and Alarm (Level 1)
Room 1 serves as the first line of defense. A Passive Infrared (PIR) motion sensor detects movement within the monitored area. When motion is detected, the system activates a visual LED strobe and an audible buzzer to alert nearby personnel.

The system can be armed or disarmed using a physical push button, allowing manual control of the security state. This room is designed to provide immediate awareness of unauthorized movement while minimizing complexity.

---

### Room 2 – Pressure-Based Countermeasure (Level 2)
Room 2 is designed to protect sensitive hard-copy materials. A Force Sensitive Resistor (FSR) detects applied pressure, such as an intruder stepping on a designated area. Upon detection, a water pump is activated via a relay module, releasing water at a controlled rate to simulate document destruction.

This subsystem requires PIN-based authorization for arming and disarming, preventing accidental activation and ensuring only authorized users can control the countermeasure. Remote backups of sensitive data are assumed to exist outside the system to maintain data integrity.

---

### Room 3 – Laser Tripwire and Mist Deterrent (Level 3)
Room 3 represents the highest security level. A laser and Light Dependent Resistor (LDR) form a tripwire mechanism. Interruption of the laser beam triggers an ultrasonic humidifier, releasing mist to simulate a gas-based deterrent.

During activation, an LCD display continuously presents a security breach message to reinforce the deterrent effect. The system requires a command-based arming sequence and a passphrase to disarm, adding an additional authentication layer.

---

## Ultrasonic Radar System (Optional Subsystem)
An external ultrasonic radar system provides early detection outside the facility. A servo motor sweeps an ultrasonic distance sensor across a 180-degree range. Distance and angle measurements are transmitted from the Raspberry Pi to a Processing-based graphical interface over a TCP/IP socket connection.

The radar visualization displays detected objects in real time, providing operators with situational awareness before an intrusion reaches the internal security layers. Password-based authentication is required to activate the radar system.

---

## Technology Stack

### Hardware
- Raspberry Pi 4 Model B
- PIR Motion Sensor
- Force Sensitive Resistor (FSR)
- Laser Module and LDR
- Ultrasonic Distance Sensor (HC-SR04)
- Servo Motor
- Relay Module
- Water Pump
- Ultrasonic Humidifier
- LCD1602 I2C Display
- USB Cameras (optional surveillance)

### Software
- Python 3
- Raspberry Pi OS
- Processing IDE (radar visualization)
- MotionEyeOS (optional surveillance)

### Communication
- GPIO-based control
- TCP/IP socket communication for radar data transmission

---

## Repository Structure
The repository is organized by functional modules to maintain separation of concerns:

- Room1: Motion detection and alarm logic
- Room2: Pressure-based countermeasure logic
- Room3: Laser tripwire and deterrent logic
- RadarSystem: Ultrasonic radar control and visualization
- media: Diagrams and screenshots used for documentation

Each module can be modified or extended independently without affecting other system components.

---

## Execution Notes
This project was developed and tested using physical hardware components. Execution requires a Raspberry Pi configured with appropriate sensors and peripherals. The repository is intended for demonstration, documentation, and review purposes rather than direct deployment without hardware setup.

---

## Design Challenges and Lessons Learned
Key challenges encountered during development included sensor calibration to reduce false positives, synchronizing multiple subsystems, and maintaining reliable TCP/IP communication between the Raspberry Pi and the radar visualization interface.

Addressing these challenges reinforced the importance of modular design, incremental testing, and clear separation between hardware control and visualization logic.

---

## Future Enhancements
Planned enhancements include improved centralized user interfaces, expanded logging of security events, cloud-based monitoring integration, additional environmental sensors, and enhanced radar resolution through advanced processing techniques.
