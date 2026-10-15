"""
EMG Mouse Control — host-side serial to mouse mapper.

Reads comma-separated filtered EMG values from the RP2040-Zero
(e.g. "512,423") and moves the OS cursor with pyautogui.

Original project: Waveshare RP2040-Zero + 2x Muscle BioAmp Patchy.
Firmware: firmware/emg_firmware.ino (115200 baud, 50 ms loop).

Usage:
    pip install -r requirements.txt
    python emg_mouse.py --port /dev/ttyACM0 --baud 115200
    python emg_mouse.py --port COM13 --baud 115200   # Windows
    python emg_mouse.py --list-ports                 # discover ports

Controls:
    Ctrl+C to exit cleanly.

Tuning:
    --smin/--smax : input sensor range (default 0..1023)
    --mmin/--mmax : mouse delta per frame (default -10..10)
    --delay       : loop delay in seconds (default 0.05)
    --deadzone    : ignore |value| below this after mapping (default 0.5 px)
"""

from __future__ import annotations

import argparse
import sys
import time


def map_range(value: float, left_min: float, left_max: float,
              right_min: float, right_max: float) -> float:
    """Linearly map value from [left_min, left_max] to [right_min, right_max]."""
    left_span = left_max - left_min
    right_span = right_max - right_min
    if left_span == 0:
        return right_min
    value_scaled = float(value - left_min) / float(left_span)
    return right_min + (value_scaled * right_span)


def list_serial_ports() -> None:
    try:
        from serial.tools import list_ports
    except ImportError:
        print("pyserial not installed. Run: pip install -r requirements.txt")
        return
    print("Available serial ports:")
    for p in list_ports.comports():
        print(f"  {p.device:20s} {p.description}")


def parse_args(argv=None):
    ap = argparse.ArgumentParser(description="EMG serial -> mouse mapper")
    ap.add_argument("--port", default="/dev/ttyACM0",
                    help="Serial port (e.g. /dev/ttyACM0, COM13)")
    ap.add_argument("--baud", type=int, default=115200, help="Baud rate")
    ap.add_argument("--smin", type=float, default=0, help="Sensor min")
    ap.add_argument("--smax", type=float, default=1023, help="Sensor max")
    ap.add_argument("--mmin", type=float, default=-10, help="Mouse delta min (px)")
    ap.add_argument("--mmax", type=float, default=10, help="Mouse delta max (px)")
    ap.add_argument("--delay", type=float, default=0.05, help="Loop delay (s)")
    ap.add_argument("--deadzone", type=float, default=0.5,
                    help="Ignore smaller mouse deltas (px)")
    ap.add_argument("--no-failsafe", action="store_true",
                    help="Disable pyautogui failsafe (corner abort)")
    ap.add_argument("--list-ports", action="store_true")
    return ap.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)

    if args.list_ports:
        list_serial_ports()
        return 0

    try:
        import serial
    except ImportError:
        print("Missing dependency: pyserial. Run: pip install -r requirements.txt")
        return 1
    try:
        import pyautogui
    except ImportError:
        print("Missing dependency: pyautogui. Run: pip install -r requirements.txt")
        return 1

    if args.no_failsafe:
        pyautogui.FAILSAFE = False

    print(f"Connecting to {args.port} @ {args.baud} ... "
          f"(Ctrl+C to quit, corner = abort unless --no-failsafe)")
    try:
        ser = serial.Serial(args.port, args.baud, timeout=1)
    except serial.SerialException as e:
        print(f"Could not open {args.port}: {e}")
        list_serial_ports()
        return 1

    time.sleep(2)  # wait for MCU reset / connection to establish
    ser.reset_input_buffer()
    print("Connected. Move muscles to move the cursor...")

    try:
        while True:
            try:
                raw = ser.readline().decode("utf-8", errors="ignore").strip()
            except serial.SerialException as e:
                print(f"Serial error: {e}")
                time.sleep(0.2)
                continue

            if not raw:
                continue

            parts = raw.split(",")
            if len(parts) != 2:
                continue

            try:
                sensor_x = int(float(parts[0]))
                sensor_y = int(float(parts[1]))
            except ValueError:
                continue

            mouse_x = map_range(sensor_x, args.smin, args.smax,
                                args.mmin, args.mmax)
            mouse_y = map_range(sensor_y, args.smin, args.smax,
                                args.mmin, args.mmax)

            # Deadzone to suppress jitter around rest.
            if abs(mouse_x) < args.deadzone:
                mouse_x = 0
            if abs(mouse_y) < args.deadzone:
                mouse_y = 0

            if mouse_x == 0 and mouse_y == 0:
                time.sleep(args.delay)
                continue

            try:
                pyautogui.moveRel(mouse_x, mouse_y)
            except pyautogui.FailSafeException:
                print("\nPyAutoGUI failsafe triggered (cursor in corner). Exiting.")
                break

            time.sleep(args.delay)

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        ser.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
