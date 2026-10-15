# Presentation outline (17 slides)

Source: `originals/Team_1-presentation.pptx` / `.pdf`
Title: **EMG-Based Assistive Device for Enhanced Human Computer Interaction**
Course: Signals and Systems — Project Based Learning
Supervisor: Dr. Raghu Indrakanti | ECE-B: Rujul Rumale (23EG104B51), Sai Vignesh (23EG104B49)

1. **Title** — project title, supervisor, team, Anurag University ECE.
2. **Problem Statements** — need for assistive HCI; fine-motor dependence;
   amputee/wrist-impairment exclusion.
3. **Solution / Objectives** — muscle-as-input interface; EMG→mouse;
   noise filtering + thresholding; real-world validation.
4. **Process** — acquire EMG → bandpass / filtration / amplification →
   send to PC → mouse movement. Figure: `figures/signal-processing-pipeline.png`.
5. **Implementation: Hardware** — Waveshare RP2040-Zero (Cortex-M0+, 12-bit ADC);
   2× Muscle BioAmp Patchy (band-pass 72–720 Hz). Photos in `figures/`.
6. **Wiring diagram** (image-only) — `figures/wiring-rp2040-two-patchy.png`:
   RP2040-Zero + two Patchy boards.
7. **System flow** (image-only) — `figures/system-flow-emg-to-mouse.png`:
   EMG Sensor → RP2040 Zero → Processing → Transfer to Computer →
   Map as Mouse Movements → Trigger mouse movement.
8. **Implementation: Software** — Arduino IDE + Python, libs `serial`,
   `pyautogui`, `time`, `csv`.
9. **Python mapping flow** (image-only) — `figures/python-mapping-flow.png`:
   Data from RP2040 → Allocate to X,Y → Map values to mouse vectors.
10. **Implementation: Signal Processing** — thresholding (deliberate activity
    only), moving-average smoothing, amplification (~3.3 V front end),
    real-time loop.
11. **Signal-processing pipeline** (image-only) — `figures/signal-processing-pipeline.png`:
    Raw → Threshold to baseline → Moving average → Amplify → Map 0–1024 → Trigger.
12. **Results plot** (image-only) — `figures/matlab-muscle-sensor-data-over-time.jpg`:
    8-panel MATLAB figure (Raw / Clamped / Stabilized / Output × Sensor 1/2).
13. **Testing & Validation** — Serial Plotter check; Python `serial` → CSV;
    MATLAB CSV plots; `pyautogui` mouse test.
14. **Final Report & Analysis / Takeaways** — hands-free input works; good
    accuracy/responsiveness with headroom; extensible to robot arms, etc.
15. **Future Upgrades** — multichannel control, leaner algorithms, boxcar/Gaussian
    filters, on-the-go sensitivity, effortless mouse-mapping (no hard flex).
16. **Conclusion** — acquired + filtered EMG; EMG→mouse vector mapping achieved;
    lessons in DSP algorithms.
17. **Thank You**.
