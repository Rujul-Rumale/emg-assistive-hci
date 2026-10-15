/*
 * EMG Mouse Firmware — Muscle Sensor Data Acquisition
 *
 * Board: Waveshare RP2040-Zero (Arduino core for RP2040)
 * Sensors: 2x Upside Down Labs Muscle BioAmp Patchy (OUT -> A0, A1)
 *
 * Pipeline:
 *   analogRead(A0/A1) -> threshold (baseline clamp) -> map 0..maxSensorRange to 0..1023
 *   -> moving-average (circular buffer) -> Serial "avg1,avg2" @ 115200 baud
 *
 * Host expects lines like: "512,423"
 * See: software/emg_mouse.py
 */

const int kBufferSize = 15;
int sensorBuffer1[kBufferSize];
int sensorBuffer2[kBufferSize];
int bufferIndex = 0;

// Anything below this raw ADC value is treated as rest/noise and clamped to 0.
// Tune per user / electrode placement (paper used 800; slides show 900 in one snippet).
const int kThreshold = 800;

// Expected active range above threshold. Remaining delta is amplified via map()
// to 0..1023 for full-resolution mouse control.
const int kMaxSensorRange = 26;

void setup() {
  Serial.begin(115200);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);

  for (int i = 0; i < kBufferSize; i++) {
    sensorBuffer1[i] = 0;
    sensorBuffer2[i] = 0;
  }
}

void loop() {
  int sensorValue1 = analogRead(A0);
  int sensorValue2 = analogRead(A1);

  // Thresholding: ignore weak baseline activity.
  if (sensorValue1 < kThreshold) {
    sensorValue1 = 0;
  } else {
    sensorValue1 = sensorValue1 - kThreshold;
  }

  if (sensorValue2 < kThreshold) {
    sensorValue2 = 0;
  } else {
    sensorValue2 = sensorValue2 - kThreshold;
  }

  // Amplitude scaling to full digital range.
  int amplifiedValue1 = map(sensorValue1, 0, kMaxSensorRange, 0, 1023);
  int amplifiedValue2 = map(sensorValue2, 0, kMaxSensorRange, 0, 1023);

  // Circular buffer + moving average for smoothing.
  sensorBuffer1[bufferIndex] = amplifiedValue1;
  sensorBuffer2[bufferIndex] = amplifiedValue2;
  bufferIndex = (bufferIndex + 1) % kBufferSize;

  int averageValue1 = calculateMovingAverage(sensorBuffer1);
  int averageValue2 = calculateMovingAverage(sensorBuffer2);

  Serial.print(averageValue1);
  Serial.print(",");
  Serial.println(averageValue2);

  delay(50);  // ~20 Hz output rate
}

int calculateMovingAverage(int *buffer) {
  long sum = 0;
  for (int i = 0; i < kBufferSize; i++) {
    sum += buffer[i];
  }
  return (int)(sum / kBufferSize);
}
