"""
Project Citadel — Room 1: Motion Detection & Alerting

Implements first-level intrusion detection using a PIR motion sensor.
When armed, motion triggers:
- LED strobe indication
- Audible alert using PWM on a buzzer/speaker output

Controls:
- Arm/Disarm via push button
- Clean shutdown on Ctrl+C (SIGINT)

GPIO Pins (BCM):
- LED: 18
- Buzzer/Speaker (PWM): 19
- PIR Motion Sensor: 25
- Arm/Disarm Button: 20
"""

from gpiozero import LED, Button, MotionSensor, Device
from gpiozero.pins.pigpio import PiGPIOFactory
from signal import pause, signal, SIGINT
import time
import sys

Device.pin_factory = PiGPIOFactory()

LED_PIN = 18
BUZZER_PWM_PIN = 19
PIR_PIN = 25
BUTTON_PIN = 20

ALERT_COOLDOWN_S = 2.0
BEEP_FREQ_HZ = 1000
BEEP_DURATION_S = 0.2
PWM_DUTY_CYCLE = 500000  # 50% (range: 0–1,000,000)

led = LED(LED_PIN)
pir = MotionSensor(PIR_PIN)
button = Button(BUTTON_PIN)

system_armed = False
last_alert_ts = 0.0


def buzzer_beep(frequency_hz: int = BEEP_FREQ_HZ, duration_s: float = BEEP_DURATION_S) -> None:
    """Generate a short audible alert using hardware PWM."""
    Device.pin_factory.hardware_PWM(BUZZER_PWM_PIN, frequency_hz, PWM_DUTY_CYCLE)
    time.sleep(duration_s)
    Device.pin_factory.hardware_PWM(BUZZER_PWM_PIN, 0, 0)


def handle_motion() -> None:
    """Triggered by PIR motion events when the system is armed."""
    global last_alert_ts

    if not system_armed:
        return

    now = time.time()
    if now - last_alert_ts < ALERT_COOLDOWN_S:
        return

    last_alert_ts = now
    print("[ALERT] Motion detected (Room 1).")

    led.blink(on_time=0.1, off_time=0.1)
    buzzer_beep()


def toggle_system() -> None:
    """Arm/disarm the Room 1 subsystem."""
    global system_armed

    system_armed = not system_armed
    if system_armed:
        print("[INFO] Room 1 armed.")
        pir.when_motion = handle_motion
    else:
        print("[INFO] Room 1 disarmed.")
        pir.when_motion = None
        led.off()
        Device.pin_factory.hardware_PWM(BUZZER_PWM_PIN, 0, 0)


def cleanup_and_exit(signum, frame) -> None:
    """Graceful shutdown: disable events and ensure outputs are off."""
    print("\n[INFO] Shutting down Room 1...")
    pir.when_motion = None
    led.off()
    try:
        Device.pin_factory.hardware_PWM(BUZZER_PWM_PIN, 0, 0)
    except Exception:
        pass
    try:
        led.close()
    except Exception:
        pass
    sys.exit(0)


button.when_pressed = toggle_system
signal(SIGINT, cleanup_and_exit)

print("Room 1 ready. Use the button to arm/disarm. Press Ctrl+C to exit.")
pause()
