# Import necessary modules
from gpiozero import LED, Button, MotionSensor, Device
from gpiozero.pins.pigpio import PiGPIOFactory
from signal import pause, signal, SIGINT
import time
import sys

# Set pigpio as the pin factory
Device.pin_factory = PiGPIOFactory()

# Define GPIO pins
LED_PIN = 18
SPEAKER_PIN = 19  # Speaker connected to GPIO 19
PIR_PIN = 25
BUTTON_PIN = 20

# Initialize components
led = LED(LED_PIN)
pir = MotionSensor(PIR_PIN)
button = Button(BUTTON_PIN)
system_armed = False

# Function to generate a simple beep sound using the speaker
def beep(frequency=1000, duration=0.2):
    print("Alarm sound on...")
    Device.pin_factory.hardware_PWM(SPEAKER_PIN, frequency, 500000)  # 50% duty cycle
    time.sleep(duration)
    Device.pin_factory.hardware_PWM(SPEAKER_PIN, 0, 0)  # Turn off the speaker

# Function to arm/disarm the system
def toggle_system():
    global system_armed
    system_armed = not system_armed
    if system_armed:
        print("Security system armed")
        pir.when_motion = handle_motion  # Re-enable motion detection when armed
    else:
        print("Security system disarmed")
        led.off()  # Turn off LED when disarming
        pir.when_motion = None  # Disable motion detection when disarmed

# Function to handle motion detection
def handle_motion():
    if system_armed:
        print("Motion detected!")
        led.blink(on_time=0.1, off_time=0.1)  # LED flashes fast like a strobe
        beep()  # Generate an alarm sound
        time.sleep(2)  # Delay to avoid over-sensitivity

# Cleanup function for graceful shutdown
def cleanup_and_exit(signum, frame):
    print("Shutting down the system...")
    led.off()
    pir.when_motion = None
    sys.exit(0)

# Event handlers
button.when_pressed = toggle_system

# Catch Ctrl+C for cleanup
signal(SIGINT, cleanup_and_exit)

# Prevent program from exiting (allow Ctrl+C to exit)
print("Press button to arm/disarm the system.")
pause()
