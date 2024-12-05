# Project Citadel - Nineveh Shadow Ops Facility

## 🛡️ Overview
**Project Citadel** is an advanced security system designed to protect high-value, sensitive areas. This system integrates cutting-edge technologies like radar, sensors, and automation to detect, deter, and respond to potential security breaches effectively.

The project demonstrates a blend of **cybersecurity principles**, **IoT innovation**, and **Python development skills**, making it a robust prototype for real-world applications.

---

## 🚀 Features
1. **Room 1: Motion Detection**
   - Equipped with a PIR sensor for motion detection.
   - Activates an LED strobe light and an audible alarm upon detecting movement.
   - Toggle system arming/disarming via a button interface.

2. **Room 2: Intruder Trap**
   - Utilizes a force-sensitive resistor (FSR) to detect unauthorized access.
   - Triggers a water pump to flood the room as a countermeasure.
   - Protected by an authorization PIN to arm and disarm the system.

3. **Room 3: Gas Release Simulation**
   - Incorporates an LDR-based laser tripwire for breach detection.
   - Activates an ultrasonic humidifier and displays a breach message on an LCD.
   - Disarmed using a passphrase (`PhantomMist`).

4. **Radar System: Proximity Monitoring**
   - Implements a servo-controlled ultrasonic radar to scan for objects.
   - Sends real-time data to a Processing-based GUI for visualization.
   - Detects objects within 40 cm and logs the distance and angle.

---

## 📂 Folder Structure
Project-Citadel/ │ ├── Room1/ │ ├── room1_pir_sensor.py # Code for motion detection and alarm system │ ├── Room2/ │ ├── room2-test.py # Code for the intruder trap with FSR │ ├── Room3/ │ ├── room3-test.py # Code for gas release simulation │ ├── RadarSystem/ │ ├── radar.py # Python code for the radar system │ ├── Radar.pde # Processing code for radar GUI visualization │ └── README.md # Project documentation


---

## 🔧 Hardware Components
- Raspberry Pi (Any model with GPIO support)
- PIR Sensor
- Force-Sensitive Resistor (FSR)
- Ultrasonic Sensor (HC-SR04)
- Servo Motor
- Ultrasonic Humidifier
- Laser Module + LDR
- LCD1602 I2C Display
- 4-Channel Relay Module
- Water Pump
- LEDs, Wires, and Breadboard

---

## 📜 Software Requirements
- **Python 3.x**
- **Libraries**:
  - gpiozero
  - RPLCD
  - RPi.GPIO
- **Processing IDE** (for radar visualization)

---

## 🖥️ How to Run
1. Clone this repository:
   ```bash
   git clone https://github.com/mr-robot1552/Project-Citadel.git

Install required Python libraries:

bash
Copy code
pip install gpiozero RPLCD RPi.GPIO
Run the scripts for each room and radar system:

Room 1: python3 room1/room1_pir_sensor.py
Room 2: python3 room2/room2-test.py
Room 3: python3 room3/room3-test.py
Radar: python3 RadarSystem/radar.py
Open the Processing IDE and load RadarSystem/Radar.pde for GUI visualization.

🌟 Highlights
Cybersecurity Integration: Each room features unique countermeasures against intrusion.
Real-time Monitoring: The radar system provides live proximity updates via a GUI.
Scalable Design: Modular architecture makes it easy to add or modify components.
🛠️ Challenges Faced
Calibrating sensor sensitivity to reduce false alarms.
Synchronizing multiple systems for seamless operation.
Debugging TCP communication for the radar's Processing GUI.
💡 Future Enhancements
Add camera modules for real-time video surveillance.
Integrate with a mobile app for remote monitoring.
Improve breach countermeasures with additional sensors and actuators.
📧 Contact
Feel free to reach out if you have questions or suggestions about this project
