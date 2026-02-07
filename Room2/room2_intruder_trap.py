"""
Project Citadel — Room 2: Intruder Trap System

Simulates a pressure-triggered trap using an FSR input. When triggered:
- Activates a relay-controlled pump
- Requires an authorization PIN to arm/disarm

GPIO Pins (BCM):
- FSR input: 26
- Relay output: 21
"""

import os
import sys
import time
from gpiozero import Button, DigitalOutputDevice, Device
from gpiozero.pins.pigpio import PiGPIOFactory

Device.pin_factory = PiGPIOFactory()

FSR_PIN = 26
RELAY_PIN = 21

DEBOUNCE_S = 0.5
IDLE_DELAY_S = 0.1

# Authorization gate (no hardcoded secret in source code)
REQUIRE_PIN = os.getenv("ROOM2_REQUIRE_PIN", "true").lower() in ("1", "true", "yes")
AUTH_PIN = os.getenv("ROOM2_AUTH_PIN", "")  # set in environment when running

fsr_trigger = Button(FSR_PIN, pull_up=False)
pump_relay = DigitalOutputDevice(RELAY_PIN, active_high=True, initial_value=False)


def require_authorization(prompt: str) -> None:
    """Prompt for an authorization PIN if enabled."""
    if not REQUIRE_PIN:
        return

    if not AUTH_PIN:
        print("[WARN] ROOM2_REQUIRE_PIN=true but ROOM2_AUTH_PIN is not set. Continuing without PIN gating.")
        return

    entered = input(prompt).strip()
    if entered != AUTH_PIN:
        print("Incorrect PIN. Exiting.")
        raise SystemExit(1)


def disarm_prompt_loop() -> None:
    """Loop until the correct PIN is entered (if gating is enabled)."""
    if not REQUIRE_PIN:
        return

    if not AUTH_PIN:
        return

    while True:
        entered = input("Enter PIN to disarm: ").strip()
        if entered == AUTH_PIN:
            print("[INFO] System disarmed. Pump deactivated.")
            pump_relay.off()
            return
        print("Incorrect PIN. System remains active.")


def monitor_fsr() -> None:
    """Continuously monitor the FSR trigger and activate the relay when pressed."""
    print("[INFO] Monitoring FSR trigger (Room 2). Press Ctrl+C to exit.")
    while True:
        if fsr_trigger.is_pressed:
            print("[ALERT] Intruder detected (Room 2). Activating pump.")
            pump_relay.on()
            time.sleep(DEBOUNCE_S)
            disarm_prompt_loop()
        else:
            pump_relay.off()
        time.sleep(IDLE_DELAY_S)


def cleanup_and_exit() -> None:
    """Ensure outputs are safe on exit."""
    print("\n[INFO] Shutting down Room 2...")
    try:
        pump_relay.off()
    except Exception:
        pass
    try:
        pump_relay.close()
    except Exception:
        pass
    raise SystemExit(0)


if __name__ == "__main__":
    try:
        pump_relay.off()
        require_authorization("Enter authorization PIN to arm Room 2: ")
        print("[INFO] Room 2 armed.")
        monitor_fsr()
    except KeyboardInterrupt:
        cleanup_and_exit()
