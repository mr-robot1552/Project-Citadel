"""
Project Citadel — Room 3: Gas Release Simulation

Simulates a breach using a laser + LDR tripwire (RC timing). When breached:
- Activates an ultrasonic humidifier via relay to simulate gas release
- Displays a persistent breach message on an I2C LCD
- Requires a passphrase to disarm (configured at runtime)

GPIO Pins (BCM):
- LDR RC input: 17
- Relay output: 23

LCD:
- I2C expander: PCF8574
- Address: 0x27 (may vary by hardware)
"""

import os
import time
from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO

# ----------------------------
# Configuration (edit safely)
# ----------------------------
LDR_PIN = 17
RELAY_PIN = 23

LCD_I2C_ADDRESS = int(os.getenv("ROOM3_LCD_ADDR", "0x27"), 16)

TRIP_THRESHOLD = int(os.getenv("ROOM3_TRIP_THRESHOLD", "2000"))
POLL_DELAY_S = 0.5
DISCHARGE_DELAY_S = 0.1

REQUIRE_PASSPHRASE = os.getenv("ROOM3_REQUIRE_PASSPHRASE", "true").lower() in ("1", "true", "yes")
DISARM_PASSPHRASE = os.getenv("ROOM3_DISARM_PASSPHRASE", "")  # set at runtime


# LCD Initialization
lcd = CharLCD("PCF8574", LCD_I2C_ADDRESS)
lcd.clear()

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)

armed = False
breach_triggered = False


def rc_time(pin: int) -> int:
    """Measure RC charge time; higher count indicates lower light (beam interrupted)."""
    count = 0
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)
    time.sleep(DISCHARGE_DELAY_S)
    GPIO.setup(pin, GPIO.IN)

    while GPIO.input(pin) == GPIO.LOW:
        count += 1

    return count


def arm_system() -> None:
    """Prompt to arm the system."""
    global armed
    while True:
        command = input("Type 'ARM' to arm Room 3: ").strip()
        if command.upper() == "ARM":
            lcd.clear()
            lcd.write_string("System Armed")
            time.sleep(1.5)
            lcd.clear()
            armed = True
            print("[INFO] Room 3 armed (laser tripwire active).")
            return


def show_breach_message() -> None:
    """Display breach status on the LCD."""
    lcd.clear()
    lcd.write_string("SECURITY BREACH")
    lcd.crlf()
    lcd.write_string("GAS RELEASED")


def set_humidifier(on: bool) -> None:
    """Control relay power to the humidifier."""
    GPIO.output(RELAY_PIN, GPIO.HIGH if on else GPIO.LOW)


def disarm_loop() -> None:
    """Prompt for passphrase until disarmed (if enabled)."""
    global armed, breach_triggered

    if not REQUIRE_PASSPHRASE:
        print("[INFO] Passphrase gate disabled. Disarming.")
        armed = False
        breach_triggered = False
        return

    if not DISARM_PASSPHRASE:
        print("[WARN] ROOM3_REQUIRE_PASSPHRASE=true but ROOM3_DISARM_PASSPHRASE is not set.")
        print("[INFO] Disarming without passphrase.")
        armed = False
        breach_triggered = False
        return

    while True:
        entered = input("Enter passphrase to disarm: ").strip()
        if entered == DISARM_PASSPHRASE:
            print("[INFO] Room 3 disarmed.")
            lcd.clear()
            lcd.write_string("System Disarmed")
            time.sleep(1.5)
            lcd.clear()
            armed = False
            breach_triggered = False
            return
        print("Incorrect passphrase. System remains active.")


def trigger_breach() -> None:
    """Activate breach response and wait for disarm."""
    global breach_triggered
    breach_triggered = True

    print("[ALERT] SECURITY BREACH detected (Room 3).")
    print("[ALERT] Countermeasures activated: gas release simulation.")

    set_humidifier(True)
    show_breach_message()

    disarm_loop()
    set_humidifier(False)


def cleanup() -> None:
    """Ensure hardware is left in a safe state."""
    try:
        set_humidifier(False)
    except Exception:
        pass
    try:
        lcd.clear()
    except Exception:
        pass
    try:
        GPIO.cleanup()
    except Exception:
        pass
    print("[INFO] Room 3 shutdown complete.")


if __name__ == "__main__":
    try:
        arm_system()
        while armed:
            light_level = rc_time(LDR_PIN)
            if light_level > TRIP_THRESHOLD and not breach_triggered:
                trigger_breach()
            time.sleep(POLL_DELAY_S)

    except KeyboardInterrupt:
        print("\n[INFO] Program interrupted by user (Ctrl+C).")

    finally:
        cleanup()
