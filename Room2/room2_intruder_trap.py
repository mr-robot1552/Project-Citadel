# Import necessary modules
from gpiozero import Button, DigitalOutputDevice, Device
from gpiozero.pins.pigpio import PiGPIOFactory
import time
import sys

# Set pigpio as the pin factory
Device.pin_factory = PiGPIOFactory()

# Define GPIO pins
FSR_PIN = 26  # GPIO pin connected to the FSR
RELAY_PIN = 21  # GPIO pin connected to the relay

# Set up components
fsr_button = Button(FSR_PIN, pull_up=False)  # Configure FSR with internal pull-down
pump_relay = DigitalOutputDevice(RELAY_PIN, active_high=True, initial_value=False)  # Ensure relay starts in the off state

# Authorization PIN
AUTH_PIN = "011010"

# Function to arm the system
def arm_system():
    entered_pin = input("For security, type your authorization PIN to enable the alarm system: ")
    if entered_pin == AUTH_PIN:
        print("System armed!")
        monitor_fsr()
    else:
        print("Incorrect PIN. System not armed.")
        sys.exit()

# Function to monitor FSR
def monitor_fsr():
    try:
        while True:
            if fsr_button.is_pressed:
                print("Intruder detected! Security breach in progress. Take immediate action.")
                pump_relay.on()  # Turn on the pump only when the FSR is pressed
                time.sleep(0.5)  # Brief delay to debounce

                disarm_system()  # Prompt to disarm after triggering
            else:
                pump_relay.off()  # Ensure pump remains off if no pressure detected
            time.sleep(0.1)  # Short delay to reduce CPU usage
    except KeyboardInterrupt:
        cleanup()

# Function to disarm the system
def disarm_system():
    entered_pin = input("Enter PIN to disarm: ")
    if entered_pin == AUTH_PIN:
        print("System disarmed. Pump deactivated.")
        pump_relay.off()
    else:
        print("Incorrect PIN. System remains active.")
        disarm_system()  # Retry until correct PIN is entered

# Function to handle cleanup on exit
def cleanup():
    print("Shutting down the system...")
    pump_relay.off()  # Ensure pump is off
    sys.exit()

# Main script execution
if __name__ == "__main__":
    pump_relay.off()  # Ensure pump is off before starting
    arm_system()
