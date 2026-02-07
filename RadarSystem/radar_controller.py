"""
Project Citadel — Radar Controller (Raspberry Pi)

Controls:
- HC-SR04 ultrasonic distance sensing (gpiozero DistanceSensor)
- Servo sweep (gpiozero Servo)
- Streams angle + distance (cm) to a Processing GUI over TCP as: "angle,distance\n"

Safety/Portfolio Notes:
- No hardcoded passwords (uses RADAR_PASSWORD env var if you want gating)
- Defaults to localhost binding for safer demos
"""

import os
import socket
import time
from gpiozero import DistanceSensor, Servo, Device
from gpiozero.pins.pigpio import PiGPIOFactory

# ----------------------------
# Configuration (edit safely)
# ----------------------------
TRIG_PIN = 6
ECHO_PIN = 13
SERVO_PIN = 5

MAX_DISTANCE_M = 1.0          # DistanceSensor max_distance (meters)
SWEEP_STEP_DEG = 5
SWEEP_DELAY_S = 0.05
ALERT_DISTANCE_CM = 40

TCP_HOST = os.getenv("RADAR_TCP_HOST", "127.0.0.1")   
TCP_PORT = int(os.getenv("RADAR_TCP_PORT", "5005"))

# Optional: password gate (set RADAR_PASSWORD in your environment)
REQUIRE_PASSWORD = os.getenv("RADAR_REQUIRE_PASSWORD", "true").lower() in ("1", "true", "yes")
RADAR_PASSWORD = os.getenv("RADAR_PASSWORD", "")  

def require_password_gate() -> None:
    """Optional password prompt gate (no hardcoded secrets)."""
    if not REQUIRE_PASSWORD:
        return

    if not RADAR_PASSWORD:
        print("[WARN] RADAR_REQUIRE_PASSWORD=true but RADAR_PASSWORD is not set. Continuing without a password gate.")
        return

    user = input("Enter the password to activate the radar: ").strip()
    if user != RADAR_PASSWORD:
        print("Incorrect password. Exiting program.")
        raise SystemExit(1)

    print("Password accepted. Waiting for Processing connection...")


def setup_hardware():
    """Initialize pigpio pin factory, distance sensor, and servo."""
    Device.pin_factory = PiGPIOFactory()

    ultrasonic = DistanceSensor(
        echo=ECHO_PIN,
        trigger=TRIG_PIN,
        max_distance=MAX_DISTANCE_M
    )
    servo = Servo(SERVO_PIN)
    return ultrasonic, servo


def setup_server():
    """Create TCP server socket and wait for a single client."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((TCP_HOST, TCP_PORT))
    server.listen(1)
    server.settimeout(60)  # don't hang forever

    print(f"[INFO] Listening on {TCP_HOST}:{TCP_PORT} (waiting for Processing client)...")
    conn, addr = server.accept()
    conn.settimeout(5)
    print(f"[INFO] Connected: {addr}")
    return server, conn


def send_data(conn: socket.socket, angle: int, distance_cm: float) -> None:
    """Send angle and distance to Processing as 'angle,distance\\n'."""
    msg = f"{angle},{distance_cm:.2f}\n"
    conn.sendall(msg.encode("utf-8"))


def sweep_radar(ultrasonic: DistanceSensor, servo: Servo, conn: socket.socket) -> None:
    """Main radar loop: sweep servo and transmit distance readings."""
    while True:
        # 0 → 180
        for angle in range(0, 181, SWEEP_STEP_DEG):
            servo.value = (angle - 90) / 90.0
            time.sleep(SWEEP_DELAY_S)

            distance_cm = ultrasonic.distance * 100.0
            send_data(conn, angle, distance_cm)

            if distance_cm < ALERT_DISTANCE_CM:
                print(f"[ALERT] Object detected @ {angle}° | {distance_cm:.0f} cm")

        # 180 → 0
        for angle in range(180, -1, -SWEEP_STEP_DEG):
            servo.value = (angle - 90) / 90.0
            time.sleep(SWEEP_DELAY_S)

            distance_cm = ultrasonic.distance * 100.0
            send_data(conn, angle, distance_cm)

            if distance_cm < ALERT_DISTANCE_CM:
                print(f"[ALERT] Object detected @ {angle}° | {distance_cm:.0f} cm")


def main():
    require_password_gate()

    ultrasonic, servo = setup_hardware()
    server = None
    conn = None

    try:
        server, conn = setup_server()
        print("[INFO] Starting radar sweep...")
        sweep_radar(ultrasonic, servo, conn)

    except KeyboardInterrupt:
        print("\n[INFO] Program interrupted by user (Ctrl+C).")

    except socket.timeout:
        print("[ERROR] Timeout waiting for Processing client connection.")

    except (BrokenPipeError, ConnectionResetError):
        print("[ERROR] Processing client disconnected.")

    finally:
        # Clean shutdown
        try:
            if conn:
                conn.close()
        except Exception:
            pass

        try:
            if server:
                server.close()
        except Exception:
            pass

        try:
            servo.detach()
        except Exception:
            pass

        try:
            ultrasonic.close()
        except Exception:
            pass

        print("[INFO] Clean shutdown complete.")


if __name__ == "__main__":
    main()
