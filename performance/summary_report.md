# Performance Summary Report

**Selected Models:**
- BF16 Baseline
- W8A8 SQ→PTQ
- W8A8 SQ→GPTQ
- W8A16 SQ→AWQ

**Metrics:** Mean ± Max Deviation

*Max Deviation = Max(max - avg, avg - min)*

---

## BF16 Baseline

| Configuration | Latency (s) | Output Throughput (tok/s) | Overall Throughput (tok/s) |
|--------------|-------------|---------------------------|----------------------------|
| Base Configuration (32,256,32) | 0.62 ± 0.02 | 3783.78 ± 27.86 | 14936.69 ± 442.74 |
| Small Batch Interactive (1,128,64) | 0.52 ± 0.04 | 132.75 ± 9.85 | 366.68 ± 24.90 |
| Long Input (1,2048,32) | 0.36 ± 0.01 | 135.23 ± 2.66 | 5806.27 ± 130.10 |
| Long Generation (1,256,512) | 3.80 ± 0.01 | 136.47 ± 0.05 | 202.36 ± 0.45 |
| Medium Batch Processing (8,256,128) | 1.07 ± 0.00 | 1072.14 ± 2.47 | 2861.12 ± 12.99 |
| High Concurrency (64,256,128) | 1.93 ± 0.02 | 6304.56 ± 27.93 | 12728.15 ± 106.09 |
| Ultra-Long Context (1,16384,32) | 1.24 ± 0.01 | 118.46 ± 2.30 | 13249.45 ± 69.71 |

---

## W8A8 SQ→PTQ

| Configuration | Latency (s) | Output Throughput (tok/s) | Overall Throughput (tok/s) |
|--------------|-------------|---------------------------|----------------------------|
| Base Configuration (32,256,32) | 0.46 ± 0.01 | 4768.20 ± 163.82 | 20078.24 ± 222.88 |
| Small Batch Interactive (1,128,64) | 0.38 ± 0.01 | 191.32 ± 3.78 | 501.29 ± 14.03 |
| Long Input (1,2048,32) | 0.27 ± 0.01 | 179.81 ± 1.79 | 7787.56 ± 172.80 |
| Long Generation (1,256,512) | 2.63 ± 0.02 | 197.63 ± 1.50 | 291.63 ± 2.26 |
| Medium Batch Processing (8,256,128) | 0.81 ± 0.00 | 1426.83 ± 4.16 | 3813.16 ± 10.80 |
| High Concurrency (64,256,128) | 1.57 ± 0.09 | 7534.97 ± 48.08 | 15701.74 ± 862.04 |
| Ultra-Long Context (1,16384,32) | 1.00 ± 0.05 | 160.89 ± 2.79 | 16365.31 ± 751.40 |

---

## W8A8 SQ→GPTQ

| Configuration | Latency (s) | Output Throughput (tok/s) | Overall Throughput (tok/s) |
|--------------|-------------|---------------------------|----------------------------|
| Base Configuration (32,256,32) | 0.46 ± 0.01 | 4800.91 ± 65.72 | 19872.25 ± 468.25 |
| Small Batch Interactive (1,128,64) | 0.39 ± 0.03 | 192.33 ± 8.64 | 495.00 ± 33.32 |
| Long Input (1,2048,32) | 0.27 ± 0.02 | 191.82 ± 11.13 | 7660.45 ± 587.88 |
| Long Generation (1,256,512) | 2.64 ± 0.01 | 197.20 ± 0.74 | 290.55 ± 1.33 |
| Medium Batch Processing (8,256,128) | 0.81 ± 0.03 | 1436.96 ± 24.49 | 3782.56 ± 121.28 |
| High Concurrency (64,256,128) | 1.52 ± 0.03 | 7581.57 ± 68.71 | 16159.96 ± 349.13 |
| Ultra-Long Context (1,16384,32) | 0.99 ± 0.01 | 162.43 ± 3.98 | 16505.70 ± 101.66 |

---

## W8A16 SQ→AWQ

| Configuration | Latency (s) | Output Throughput (tok/s) | Overall Throughput (tok/s) |
|--------------|-------------|---------------------------|----------------------------|
| Base Configuration (32,256,32) | 0.75 ± 0.01 | 3963.28 ± 46.77 | 12320.49 ± 233.05 |
| Small Batch Interactive (1,128,64) | 0.39 ± 0.02 | 180.34 ± 5.64 | 487.35 ± 26.60 |
| Long Input (1,2048,32) | 0.33 ± 0.01 | 180.59 ± 10.47 | 6266.82 ± 256.18 |
| Long Generation (1,256,512) | 2.78 ± 0.01 | 187.18 ± 0.70 | 276.22 ± 0.65 |
| Medium Batch Processing (8,256,128) | 0.90 ± 0.00 | 1368.53 ± 10.75 | 3396.03 ± 16.81 |
| High Concurrency (64,256,128) | 2.47 ± 0.01 | 5239.31 ± 12.01 | 9941.34 ± 24.48 |
| Ultra-Long Context (1,16384,32) | 1.48 ± 0.01 | 157.27 ± 1.43 | 11075.30 ± 41.35 |

---
