# Import necessary libraries
from gpiozero import DistanceSensor, Servo, Device
from gpiozero.pins.pigpio import PiGPIOFactory
import socket
import time

# Set pigpio as the pin factory
Device.pin_factory = PiGPIOFactory()

# Define GPIO pins
TRIG_PIN = 6  # GPIO 6 for Trigger
ECHO_PIN = 13  # GPIO 13 for Echo
SERVO_PIN = 5  # GPIO 5 for Servo PWM

# Set up components
ultrasonic = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN, max_distance=1)
servo = Servo(SERVO_PIN)

# Set up TCP connection for Processing
TCP_IP = '0.0.0.0'  # Use 0.0.0.0 to allow connections from any IP address
TCP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(1)

# Password-protected start
password = "watcher"
input_password = input("Enter the password to activate the radar: ")
if input_password != password:
    print("Incorrect password. Exiting program.")
    exit()
else:
    print("Password accepted. Attempting to connect...")

# Accept the connection from Processing
conn, addr = sock.accept()
print(f"Connection established with {addr}. Starting radar...")

# Function to send distance data to Processing
def send_data(angle, distance):
    message = f"{angle},{distance}\n"
    conn.send(message.encode())

# Main loop for radar sweeping and distance measurement
try:
    while True:
        # Sweep from 0 to 180 degrees and back, with slower speed
        for angle in range(0, 181, 5):
            servo.value = (angle - 90) / 90.0  # Convert to servo range
            time.sleep(0.05)  # Slow down the servo movement
            
            # Measure distance and send data to Processing
            distance = ultrasonic.distance * 100  # Convert to cm
            send_data(angle, distance)
            if distance < 40:
                print("Unidentified object detected at angle", angle, "and distance", int(distance), "cm")

        for angle in range(180, -1, -5):
            servo.value = (angle - 90) / 90.0
            time.sleep(0.05)
            
            distance = ultrasonic.distance * 100
            send_data(angle, distance)
            if distance < 40:
                print("Unidentified object detected at angle", angle, "and distance", int(distance), "cm")

except KeyboardInterrupt:
    print("Program interrupted by user")
finally:
    conn.close()
    sock.close()
    print("Socket closed")
