# Firmware

Arduino firmware for the Waveshare RP2040-Zero. Reads two Muscle BioAmp Patchy
sensors, filters, smooths, and streams `avg1,avg2` over USB serial.

## File

- `emg_firmware.ino` — flash this with Arduino IDE (RP2040 core)

## Board setup (Arduino IDE)

1. Install Arduino IDE.
2. Boards Manager → install `Raspberry Pi Pico / RP2040` core (e.g. Earle Philhower).
3. Select board: `Waveshare RP2040 Zero`.
4. Select USB port, baud is set in code to `115200`.
5. Open `emg_firmware.ino`, verify + upload.
6. Open Tools → Serial Plotter @ 115200 to verify live EMG envelopes.

## Signal chain (firmware)

```text
analogRead(A0/A1) → threshold clamp → map(0..26 → 0..1023)
  → circular buffer (15) → moving average → Serial "avg1,avg2" @ ~20 Hz
```

| Parameter | Value | Notes |
|---|---|---|
| `kThreshold` | `800` | Below = rest, clamped to 0. Tune 700–950 per user. |
| `kMaxSensorRange` | `26` | Active delta above threshold mapped to full scale. |
| `kBufferSize` | `15` | ~0.75 s window at 50 ms loop. Larger = smoother but laggier. |
| Loop delay | `50 ms` | ~20 Hz host update rate. |

## Wiring

See `../hardware/wiring.md` and `../docs/figures/wiring-rp2040-two-patchy.png`.

- Patchy 1 `OUT` → `A0` (GP26), Patchy 2 `OUT` → `A1` (GP27)
- `VCC` → `5V`, `GND` → `GND`, `REF` → reference electrode / GND
- Common ground between sensors, MCU, and PC (via USB) is required.

## Tuning tips

- If cursor never moves: lower `kThreshold` or increase `kMaxSensorRange`.
- If cursor jitters at rest: raise `kThreshold` or add deadzone in `software/emg_mouse.py`.
- If motion is laggy: reduce `kBufferSize` to 8–10.
- If one axis dominates: calibrate per-channel thresholds (split `kThreshold` into two constants).
