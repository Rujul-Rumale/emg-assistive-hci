# Report summary

Full report (33 pages, ~6,875 words): `originals/EMG_Paper_RV_V4.odt` and
`originals/EMG_Paper_RV_V4.pdf`.

Title: **EMG-Based Assistive Device for Enhanced Human-Computer Interaction**
Course: Signals and Systems — Project Based Learning, Dept. of ECE, Anurag University (2023–2024).
Authors: Rujul Rajeev Rumale (23EG104B51), G. Sai Vignesh (23EG104B49).
Supervisor: Dr. Raghu Indrakanti, Assistant Professor, Dept. of ECE.

## Abstract (from report)

> Design and implementation of an EMG-based assistive device that enhances
> human-computer interaction for individuals with motor disabilities. Muscle
> signals from various body parts are translated into mouse movements. Built
> with Muscle BioAmp Patchy + RP2040 Zero; a Python script maps serial data
> to mouse movements with `pyautogui`.

Keywords: EMG, Assistive Technology, Arduino, Human-Computer Interaction,
Muscle BioAmp Patchy, RP2040

## Chapter map

- **I — Introduction**: EMG fundamentals (generation, surface vs intramuscular
  electrodes, 0–10 mV amplitude, 20–500 Hz band, noise sensitivity),
  amplification / filtering / rectification / smoothing, assistive-device
  basics, problem statement, objectives, scope.
- **II — Literature review**: Barreto et al. (2007), Lin et al. (2008, SVM),
  Chauvin & Moreau (2008, multichannel), Akben & Temurtas (2018, ANN),
  Rojas-Martinez & Alvarez (2018, survey); gaps in cost, robustness, generality.
- **III — Existing methods**: keyboards/mice limits; voice (HMM), eye-tracking
  (Kalman), switch-based; EMG DSP (DFT, Butterworth, moving average, RMS/MAV).
- **IV — Proposed methodology**: system overview, hardware (BioAmp Patchy +
  RP2040 Zero), software (Arduino + Python), acquisition + threshold (800) +
  scaling (0–20/26 → 0–1023) + moving average.
- **V — Software description**: `analogRead(A0/A1)`, thresholding, circular
  buffer + moving average, `Serial "v1,v2"`; Python `serial` read → `map_range`
  → `pyautogui.moveRel`.
- **VI — Results & analysis**: forearm placement, cursor/icon/click tasks,
  raw → clamped → stabilized → output plots (see `figures/matlab-muscle-sensor-data-over-time.jpg`).
- **VII — Advantages & applications**: real-time, non-invasive/lightweight,
  tunable sensitivity, low extra hardware; HCI, gaming, assistive robotics,
  prosthetics, rehab.
- **VIII — Conclusion & future scope**: working EMG→mouse control; future =
  more channels, ML classification, mobile integration, wheelchair/exoskeleton,
  per-user calibration.
- **References**: 7 entries (see report Ch. VIII / README).
- **Appendix**: full Arduino firmware + Python script (recovered in
  `firmware/` and `software/`).

## Key figures in this repo

- `figures/emg-generation-principle.jpg` — neuromuscular EMG generation
- `figures/raw-emg-example.jpg` — raw EMG (relax vs contract)
- `figures/system-flow-color.png` / `system-flow-emg-to-mouse.png` — end-to-end flow
- `figures/signal-processing-color.png` / `signal-processing-pipeline.png` — DSP chain
- `figures/wiring-rp2040-two-patchy.png` — wiring diagram
- `figures/matlab-muscle-sensor-data-over-time.jpg` — validation plot (raw/clamped/stabilized/output ×2 ch)
