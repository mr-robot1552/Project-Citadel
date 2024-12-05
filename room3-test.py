import time
from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO

# LCD Initialization
lcd = CharLCD('PCF8574', 0x27)  # Replace 0x27 with your I2C address if different
lcd.clear()  # Clear the screen to initialize

# GPIO Setup
GPIO.setmode(GPIO.BCM)
LDR_PIN = 17  # GPIO pin connected to the LDR-capacitor circuit
RELAY_PIN = 23  # GPIO pin connected to the relay module for the humidifier

GPIO.setup(RELAY_PIN, GPIO.OUT)  # Set up the relay control pin as an output
GPIO.output(RELAY_PIN, GPIO.LOW)  # Ensure the relay is initially off

armed = False
breach_triggered = False

def rc_time(pin):
    """Measure the time taken for the capacitor to charge, indicative of light level."""
    count = 0
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)
    time.sleep(0.1)
    GPIO.setup(pin, GPIO.IN)

    while GPIO.input(pin) == GPIO.LOW:
        count += 1

    return count

def arm_system():
    """Prompt to arm the system."""
    global armed
    while True:
        command = input("Would you like to arm the system? Type 'ARM' to proceed: ")
        if command.upper() == "ARM":
            print("System armed!")
            lcd.write_string("System Armed!")  # Display message on the LCD
            time.sleep(2)
            lcd.clear()
            armed = True
            print("Laser tripwire armed and ready.")
            break

def trigger_breach():
    """Activate the breach message and turn on the humidifier continuously until disarmed."""
    global breach_triggered
    breach_triggered = True
    GPIO.output(RELAY_PIN, GPIO.HIGH)  # Activate the relay to power the humidifier
    print("SECURITY BREACH detected!")
    print("Countermeasures Activated - Gas Released!")

    # Display breach message on the LCD
    lcd.write_string("SECURITY BREACH!")
    lcd.crlf()
    lcd.write_string("GAS RELEASED!")
    while breach_triggered:  # Keep the message displayed until the system is disarmed
        time.sleep(1)

    disarm_system()  # Prompt to disarm immediately after breach

def disarm_system():
    """Prompt to disarm the system with passphrase."""
    global armed, breach_triggered
    while True:
        passphrase = input("Enter passphrase to disarm: ")
        if passphrase == "PhantomMist":
            print("System disarmed.")
            lcd.clear()  # Clear the LCD screen
            lcd.write_string("System Disarmed")
            time.sleep(2)
            lcd.clear()
            armed = False
            breach_triggered = False
            GPIO.output(RELAY_PIN, GPIO.LOW)  # Deactivate the relay to turn off the humidifier
            break

try:
    arm_system()
    if armed:
        while armed:
            light_level = rc_time(LDR_PIN)  # Check for breach
            if light_level > 2000 and not breach_triggered:  # Adjust threshold as needed
                trigger_breach()
            time.sleep(0.5)  # Small delay to prevent excessive polling
except KeyboardInterrupt:
    print("Program interrupted.")
    lcd.clear()  # Clear the LCD on exit
finally:
    GPIO.cleanup()
    lcd.clear()  # Ensure the LCD is cleared on exit
    print("System shutdown.")
