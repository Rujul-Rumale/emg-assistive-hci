# Software (host)

Python host side: serial → mouse cursor, plus a CSV logger for validation.

## Files

- `emg_mouse.py` — main mapper (`pyserial` + `pyautogui`)
- `log_emg.py` — CSV logger for offline analysis / MATLAB plots
- `requirements.txt`

## Install

```bash
pip install -r requirements.txt
# Linux: you may need xdotool / scrot deps for pyautogui, and dialout group:
#   sudo usermod -aG dialout $USER
```

## Run

```bash
# discover ports
python emg_mouse.py --list-ports

# Linux (RP2040 usually /dev/ttyACM0)
python emg_mouse.py --port /dev/ttyACM0 --baud 115200

# Windows
python emg_mouse.py --port COM13 --baud 115200
```

Move muscles: sensor 1 → X, sensor 2 → Y. Values `0..1023` map to `-10..10` px
per frame by default. Press `Ctrl+C` to quit. Moving the cursor to a screen
corner aborts via pyautogui failsafe (disable with `--no-failsafe`).

## Tuning

```bash
python emg_mouse.py --port /dev/ttyACM0 --mmin -15 --mmax 15 --deadzone 1.0 --delay 0.03
```

| Flag | Default | Effect |
|---|---|---|
| `--smin/--smax` | `0 / 1023` | Input range from firmware |
| `--mmin/--mmax` | `-10 / 10` | Cursor px per frame; larger = faster |
| `--deadzone` | `0.5` | Suppresses rest jitter |
| `--delay` | `0.05` | Loop pacing; smaller = more responsive, jumpier |

## Validation / logging

```bash
python log_emg.py --port /dev/ttyACM0 --out emg_log.csv --seconds 60
```

- `emg_log.csv` columns: `t_s, sensor1, sensor2, raw_line`
- Plot in MATLAB / Python to reproduce `docs/figures/matlab-muscle-sensor-data-over-time.jpg`:
  raw → clamped → stabilized → output stages.
- The project validated in three steps (per report):
  1. Arduino Serial Plotter (live envelope),
  2. Python `serial` → CSV,
  3. MATLAB plot of CSV + `pyautogui` mouse test.

## Safety note

`pyautogui` takes over your cursor. Test with small `--mmin/--mmax` first,
keep a keyboard handy for `Ctrl+C`, and do not run while doing precision work.
