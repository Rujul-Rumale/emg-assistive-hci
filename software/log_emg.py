"""
EMG serial logger — validation utility used in the project.

Saves raw "avg1,avg2" lines from the RP2040 to CSV for offline
analysis (the report validates with Arduino Serial Plotter + MATLAB).

Usage:
    python log_emg.py --port /dev/ttyACM0 --baud 115200 --out emg_log.csv
    python log_emg.py --port COM13 --out emg_log.csv --seconds 60
"""

from __future__ import annotations

import argparse
import csv
import sys
import time

import serial


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="/dev/ttyACM0")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--out", default="emg_log.csv")
    ap.add_argument("--seconds", type=float, default=0,
                    help="0 = run until Ctrl+C")
    args = ap.parse_args()

    try:
        ser = serial.Serial(args.port, args.baud, timeout=1)
    except serial.SerialException as e:
        print(f"Could not open {args.port}: {e}")
        return 1

    time.sleep(2)
    ser.reset_input_buffer()
    start = time.time()
    print(f"Logging {args.port} -> {args.out} (Ctrl+C to stop)")

    with open(args.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t_s", "sensor1", "sensor2", "raw_line"])
        try:
            while True:
                if args.seconds and (time.time() - start) > args.seconds:
                    break
                line = ser.readline().decode("utf-8", errors="ignore").strip()
                if not line:
                    continue
                t = time.time() - start
                parts = line.split(",")
                if len(parts) == 2:
                    try:
                        w.writerow([f"{t:.3f}", int(float(parts[0])),
                                    int(float(parts[1])), line])
                    except ValueError:
                        w.writerow([f"{t:.3f}", "", "", line])
                else:
                    w.writerow([f"{t:.3f}", "", "", line])
        except KeyboardInterrupt:
            print("\nStopped.")
        finally:
            ser.close()

    print(f"Saved {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
