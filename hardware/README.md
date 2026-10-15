# Hardware

## Bill of materials

| # | Part | Notes |
|---|---|---|
| 1 | Waveshare RP2040-Zero | RP2040 MCU, dual Cortex-M0+ @ 133 MHz, 12-bit ADC, USB-C, compact form factor |
| 2 | Muscle BioAmp Patchy (Upside Down Labs) ×2 | Wearable surface-EMG front end, on-board band-pass (~72–720 Hz per presentation), snap electrodes |
| 3 | EMG snap electrodes + reference electrode | Skin contact; replace/shave-prep as needed |
| 4 | USB-C data cable | MCU → PC serial (115200 baud) + power |
| 5 | PC (Windows/Linux) | Runs `software/emg_mouse.py` (Python + `pyautogui`) |

Software toolchain: Arduino IDE (firmware) + Python 3 (`serial`, `pyautogui`, `time`, `csv`) for host.

## Wiring

Full diagram: `../docs/figures/wiring-rp2040-two-patchy.png`

```text
Patchy #1 (X-axis)          RP2040-Zero          Patchy #2 (Y-axis)
  VCC  ------------------->  5V  (or 3V3)
  GND  ------------------->  GND  <-------------------  GND
  OUT  ------------------->  A0 (GP26)                 OUT  ---> A1 (GP27)
  REF  -> reference electrode (forearm/bony area) + common GND
```

Notes:

- Keep sensor `GND` and MCU `GND` common (USB provides PC ground).
- `A0/A1` in Arduino RP2040 core map to `GP26/GP27` on the Zero.
- Place the two differential snaps along the target muscle belly, reference
  on an electrically quiet spot (per BioAmp docs).
- Route sensor leads away from mains/switching supplies to reduce 50/60 Hz pickup.
- The presentation used `threshold = 800`, `map 0..26 → 0..1023`; one code
  screenshot shows `900` — treat threshold as per-user calibration, not fixed.

## Photos

- `../docs/figures/waveshare-rp2040-zero.jpg` — MCU
- `../docs/figures/muscle-bioamp-patchy-photo.jpg` / `muscle-bioamp-patchy-blue.jpg` — sensors
- `../docs/figures/wiring-rp2040-two-patchy.png` — wiring diagram

## Power / safety

- Powered from USB (no external supply needed).
- Surface electrodes only; non-invasive, low voltage.
- This is a coursework prototype, not a medical device. Do not use for diagnosis.
