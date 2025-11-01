# Performance Benchmark Results

**Generated from:** `result.jsonl`

---


## Configuration: batch_size=1, input_len=128, output_len=64

**Total models tested:** 7


### Summary Table

| Model | Runs | Latency (s) | Output Throughput (tok/s) | Overall Throughput (tok/s) | Input Throughput (tok/s) |
|-------|------|-------------|---------------------------|----------------------------|--------------------------|
| `w8a8_sparse_smooth_gptq_interactive` | 3 | 0.38 ± 0.01 | 193.82 ± 6.87 | 504.64 ± 13.05 | 0.00 |
| `w8a8_smooth_gptq_interactive` | 3 | 0.39 ± 0.02 | 192.33 ± 8.07 | 495.00 ± 29.09 | 0.00 |
| `w8a8_smooth_ptq_interactive` | 3 | 0.38 ± 0.01 | 191.32 ± 3.34 | 501.29 ± 12.16 | 0.00 |
| `w8a16_sparse_awq_interactive` | 3 | 0.39 ± 0.01 | 181.78 ± 3.64 | 488.37 ± 8.50 | 0.00 |
| `w8a16_smooth_awq_interactive` | 3 | 0.39 ± 0.02 | 180.34 ± 5.14 | 487.35 ± 24.21 | 0.00 |
| `w8a16_awq_interactive` | 3 | 0.40 ± 0.00 | 177.93 ± 1.24 | 479.99 ± 4.85 | 0.00 |
| `original_interactive` | 3 | 0.52 ± 0.03 | 132.75 ± 8.54 | 366.68 ± 21.60 | 0.00 |

### Detailed Results


#### original_interactive

- **Total runs:** 3

- **Individual runs:**

  - `original_interactive_run1`:
    - Latency: 0.51s
    - Output Throughput: 138.03 tok/s
    - Overall Throughput: 377.82 tok/s
    - Input Throughput: N/A
  - `original_interactive_run3`:
    - Latency: 0.56s
    - Output Throughput: 122.90 tok/s
    - Overall Throughput: 341.78 tok/s
    - Input Throughput: N/A
  - `original_interactive_run3`:
    - Latency: 0.50s
    - Output Throughput: 137.33 tok/s
    - Overall Throughput: 380.44 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.52 ± 0.03
  - Output Throughput: 132.75 ± 8.54
  - Overall Throughput: 366.68 ± 21.60

#### w8a16_awq_interactive

- **Total runs:** 3

- **Individual runs:**

  - `w8a16_awq_interactive_run2`:
    - Latency: 0.40s
    - Output Throughput: 177.15 tok/s
    - Overall Throughput: 485.44 tok/s
    - Input Throughput: N/A
  - `w8a16_awq_interactive_run3`:
    - Latency: 0.40s
    - Output Throughput: 177.29 tok/s
    - Overall Throughput: 476.16 tok/s
    - Input Throughput: N/A
  - `w8a16_awq_interactive_run3`:
    - Latency: 0.40s
    - Output Throughput: 179.36 tok/s
    - Overall Throughput: 478.36 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.40 ± 0.00
  - Output Throughput: 177.93 ± 1.24
  - Overall Throughput: 479.99 ± 4.85

#### w8a16_smooth_awq_interactive

- **Total runs:** 3

- **Individual runs:**

  - `w8a16_smooth_awq_interactive_run1`:
    - Latency: 0.42s
    - Output Throughput: 174.70 tok/s
    - Overall Throughput: 460.75 tok/s
    - Input Throughput: N/A
  - `w8a16_smooth_awq_interactive_run2`:
    - Latency: 0.39s
    - Output Throughput: 181.56 tok/s
    - Overall Throughput: 493.19 tok/s
    - Input Throughput: N/A
  - `w8a16_smooth_awq_interactive_run3`:
    - Latency: 0.38s
    - Output Throughput: 184.75 tok/s
    - Overall Throughput: 508.11 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.39 ± 0.02
  - Output Throughput: 180.34 ± 5.14
  - Overall Throughput: 487.35 ± 24.21

#### w8a16_sparse_awq_interactive

- **Total runs:** 3

- **Individual runs:**

  - `w8a16_sparse_awq_interactive_run1`:
    - Latency: 0.39s
    - Output Throughput: 185.82 tok/s
    - Overall Throughput: 498.08 tok/s
    - Input Throughput: N/A
  - `w8a16_sparse_awq_interactive_run2`:
    - Latency: 0.40s
    - Output Throughput: 178.76 tok/s
    - Overall Throughput: 484.77 tok/s
    - Input Throughput: N/A
  - `w8a16_sparse_awq_interactive_run3`:
    - Latency: 0.40s
    - Output Throughput: 180.75 tok/s
    - Overall Throughput: 482.27 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.39 ± 0.01
  - Output Throughput: 181.78 ± 3.64
  - Overall Throughput: 488.37 ± 8.50

#### w8a8_smooth_gptq_interactive

- **Total runs:** 3

- **Individual runs:**

  - `w8a8_smooth_gptq_interactive_run2`:
    - Latency: 0.42s
    - Output Throughput: 183.69 tok/s
    - Overall Throughput: 461.68 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_gptq_interactive_run2`:
    - Latency: 0.37s
    - Output Throughput: 199.68 tok/s
    - Overall Throughput: 515.29 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_gptq_interactive_run3`:
    - Latency: 0.38s
    - Output Throughput: 193.62 tok/s
    - Overall Throughput: 508.04 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.39 ± 0.02
  - Output Throughput: 192.33 ± 8.07
  - Overall Throughput: 495.00 ± 29.09

#### w8a8_smooth_ptq_interactive

- **Total runs:** 3

- **Individual runs:**

  - `w8a8_smooth_ptq_interactive_run1`:
    - Latency: 0.39s
    - Output Throughput: 187.54 tok/s
    - Overall Throughput: 487.26 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_ptq_interactive_run2`:
    - Latency: 0.38s
    - Output Throughput: 192.54 tok/s
    - Overall Throughput: 507.77 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_ptq_interactive_run3`:
    - Latency: 0.38s
    - Output Throughput: 193.88 tok/s
    - Overall Throughput: 508.83 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.38 ± 0.01
  - Output Throughput: 191.32 ± 3.34
  - Overall Throughput: 501.29 ± 12.16

#### w8a8_sparse_smooth_gptq_interactive

- **Total runs:** 3

- **Individual runs:**

  - `w8a8_sparse_smooth_gptq_interactive_run2`:
    - Latency: 0.37s
    - Output Throughput: 201.38 tok/s
    - Overall Throughput: 519.56 tok/s
    - Input Throughput: N/A
  - `w8a8_sparse_smooth_gptq_interactive_run2`:
    - Latency: 0.39s
    - Output Throughput: 192.15 tok/s
    - Overall Throughput: 495.31 tok/s
    - Input Throughput: N/A
  - `w8a8_sparse_smooth_gptq_interactive_run3`:
    - Latency: 0.38s
    - Output Throughput: 187.94 tok/s
    - Overall Throughput: 499.06 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.38 ± 0.01
  - Output Throughput: 193.82 ± 6.87
  - Overall Throughput: 504.64 ± 13.05

## Configuration: batch_size=1, input_len=256, output_len=512

**Total models tested:** 7


### Summary Table

| Model | Runs | Latency (s) | Output Throughput (tok/s) | Overall Throughput (tok/s) | Input Throughput (tok/s) |
|-------|------|-------------|---------------------------|----------------------------|--------------------------|
| `w8a8_sparse_smooth_gptq_decode_bound` | 3 | 2.63 ± 0.01 | 198.06 ± 0.13 | 291.80 ± 0.62 | 0.00 |
| `w8a8_smooth_ptq_decode_bound` | 3 | 2.63 ± 0.02 | 197.63 ± 1.34 | 291.63 ± 2.03 | 0.00 |
| `w8a8_smooth_gptq_decode_bound` | 3 | 2.64 ± 0.01 | 197.20 ± 0.66 | 290.55 ± 1.17 | 0.00 |
| `w8a16_sparse_awq_decode_bound` | 3 | 2.77 ± 0.02 | 188.21 ± 1.20 | 277.61 ± 1.59 | 0.00 |
| `w8a16_awq_decode_bound` | 3 | 2.77 ± 0.01 | 187.49 ± 0.56 | 276.92 ± 0.98 | 0.00 |
| `w8a16_smooth_awq_decode_bound` | 3 | 2.78 ± 0.01 | 187.18 ± 0.69 | 276.22 ± 0.58 | 0.00 |
| `original_decode_bound` | 3 | 3.80 ± 0.01 | 136.47 ± 0.05 | 202.36 ± 0.40 | 0.00 |

### Detailed Results


#### original_decode_bound

- **Total runs:** 3

- **Individual runs:**

  - `original_decode_bound_run1`:
    - Latency: 3.80s
    - Output Throughput: 136.42 tok/s
    - Overall Throughput: 202.24 tok/s
    - Input Throughput: N/A
  - `original_decode_bound_run2`:
    - Latency: 3.79s
    - Output Throughput: 136.51 tok/s
    - Overall Throughput: 202.81 tok/s
    - Input Throughput: N/A
  - `original_decode_bound_run3`:
    - Latency: 3.80s
    - Output Throughput: 136.47 tok/s
    - Overall Throughput: 202.03 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 3.80 ± 0.01
  - Output Throughput: 136.47 ± 0.05
  - Overall Throughput: 202.36 ± 0.40

#### w8a16_awq_decode_bound

- **Total runs:** 3

- **Individual runs:**

  - `w8a16_awq_decode_bound_run1`:
    - Latency: 2.78s
    - Output Throughput: 186.96 tok/s
    - Overall Throughput: 275.82 tok/s
    - Input Throughput: N/A
  - `w8a16_awq_decode_bound_run2`:
    - Latency: 2.77s
    - Output Throughput: 188.07 tok/s
    - Overall Throughput: 277.68 tok/s
    - Input Throughput: N/A
  - `w8a16_awq_decode_bound_run3`:
    - Latency: 2.77s
    - Output Throughput: 187.44 tok/s
    - Overall Throughput: 277.26 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 2.77 ± 0.01
  - Output Throughput: 187.49 ± 0.56
  - Overall Throughput: 276.92 ± 0.98

#### w8a16_smooth_awq_decode_bound

- **Total runs:** 3

- **Individual runs:**

  - `w8a16_smooth_awq_decode_bound_run1`:
    - Latency: 2.77s
    - Output Throughput: 187.86 tok/s
    - Overall Throughput: 276.87 tok/s
    - Input Throughput: N/A
  - `w8a16_smooth_awq_decode_bound_run2`:
    - Latency: 2.78s
    - Output Throughput: 186.48 tok/s
    - Overall Throughput: 276.00 tok/s
    - Input Throughput: N/A
  - `w8a16_smooth_awq_decode_bound_run3`:
    - Latency: 2.78s
    - Output Throughput: 187.19 tok/s
    - Overall Throughput: 275.78 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 2.78 ± 0.01
  - Output Throughput: 187.18 ± 0.69
  - Overall Throughput: 276.22 ± 0.58

#### w8a16_sparse_awq_decode_bound

- **Total runs:** 3

- **Individual runs:**

  - `w8a16_sparse_awq_decode_bound_run2`:
    - Latency: 2.78s
    - Output Throughput: 186.83 tok/s
    - Overall Throughput: 276.08 tok/s
    - Input Throughput: N/A
  - `w8a16_sparse_awq_decode_bound_run1`:
    - Latency: 2.77s
    - Output Throughput: 188.74 tok/s
    - Overall Throughput: 277.50 tok/s
    - Input Throughput: N/A
  - `w8a16_sparse_awq_decode_bound_run3`:
    - Latency: 2.75s
    - Output Throughput: 189.05 tok/s
    - Overall Throughput: 279.26 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 2.77 ± 0.02
  - Output Throughput: 188.21 ± 1.20
  - Overall Throughput: 277.61 ± 1.59

#### w8a8_smooth_gptq_decode_bound

- **Total runs:** 3

- **Individual runs:**

  - `w8a8_smooth_gptq_decode_bound_run1`:
    - Latency: 2.65s
    - Output Throughput: 196.46 tok/s
    - Overall Throughput: 289.67 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_gptq_decode_bound_run2`:
    - Latency: 2.63s
    - Output Throughput: 197.74 tok/s
    - Overall Throughput: 291.88 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_gptq_decode_bound_run3`:
    - Latency: 2.65s
    - Output Throughput: 197.41 tok/s
    - Overall Throughput: 290.10 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 2.64 ± 0.01
  - Output Throughput: 197.20 ± 0.66
  - Overall Throughput: 290.55 ± 1.17

#### w8a8_smooth_ptq_decode_bound

- **Total runs:** 3

- **Individual runs:**

  - `w8a8_smooth_ptq_decode_bound_run1`:
    - Latency: 2.63s
    - Output Throughput: 198.02 tok/s
    - Overall Throughput: 292.21 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_ptq_decode_bound_run2`:
    - Latency: 2.65s
    - Output Throughput: 196.13 tok/s
    - Overall Throughput: 289.37 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_ptq_decode_bound_run3`:
    - Latency: 2.62s
    - Output Throughput: 198.73 tok/s
    - Overall Throughput: 293.31 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 2.63 ± 0.02
  - Output Throughput: 197.63 ± 1.34
  - Overall Throughput: 291.63 ± 2.03

#### w8a8_sparse_smooth_gptq_decode_bound

- **Total runs:** 3

- **Individual runs:**

  - `w8a8_sparse_smooth_gptq_decode_bound_run1`:
    - Latency: 2.64s
    - Output Throughput: 197.92 tok/s
    - Overall Throughput: 291.13 tok/s
    - Input Throughput: N/A
  - `w8a8_sparse_smooth_gptq_decode_bound_run2`:
    - Latency: 2.63s
    - Output Throughput: 198.08 tok/s
    - Overall Throughput: 292.34 tok/s
    - Input Throughput: N/A
  - `w8a8_sparse_smooth_gptq_decode_bound_run3`:
    - Latency: 2.63s
    - Output Throughput: 198.18 tok/s
    - Overall Throughput: 291.93 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 2.63 ± 0.01
  - Output Throughput: 198.06 ± 0.13
  - Overall Throughput: 291.80 ± 0.62

## Configuration: batch_size=1, input_len=2048, output_len=32

**Total models tested:** 7


### Summary Table

| Model | Runs | Latency (s) | Output Throughput (tok/s) | Overall Throughput (tok/s) | Input Throughput (tok/s) |
|-------|------|-------------|---------------------------|----------------------------|--------------------------|
| `w8a16_sparse_awq_prefill_bound` | 3 | 0.32 ± 0.00 | 192.76 ± 7.99 | 6418.11 ± 75.61 | 0.00 |
| `w8a8_smooth_gptq_prefill_bound` | 3 | 0.27 ± 0.02 | 191.82 ± 10.16 | 7660.45 ± 532.10 | 0.00 |
| `w8a16_smooth_awq_prefill_bound` | 3 | 0.33 ± 0.01 | 180.59 ± 10.12 | 6266.82 ± 222.64 | 0.00 |
| `w8a8_smooth_ptq_prefill_bound` | 3 | 0.27 ± 0.01 | 179.81 ± 1.78 | 7787.56 ± 150.14 | 0.00 |
| `w8a16_awq_prefill_bound` | 3 | 0.34 ± 0.02 | 179.33 ± 10.82 | 6201.77 ± 289.72 | 0.00 |
| `w8a8_sparse_smooth_gptq_prefill_bound` | 3 | 0.27 ± 0.01 | 178.38 ± 8.69 | 7620.84 ± 368.73 | 0.00 |
| `original_prefill_bound` | 3 | 0.36 ± 0.01 | 135.23 ± 2.50 | 5806.27 ± 126.94 | 0.00 |

### Detailed Results


#### original_prefill_bound

- **Total runs:** 3

- **Individual runs:**

  - `original_prefill_bound_run1`:
    - Latency: 0.35s
    - Output Throughput: 137.54 tok/s
    - Overall Throughput: 5929.80 tok/s
    - Input Throughput: N/A
  - `original_prefill_bound_run2`:
    - Latency: 0.37s
    - Output Throughput: 132.57 tok/s
    - Overall Throughput: 5676.17 tok/s
    - Input Throughput: N/A
  - `original_prefill_bound_run3`:
    - Latency: 0.36s
    - Output Throughput: 135.58 tok/s
    - Overall Throughput: 5812.84 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.36 ± 0.01
  - Output Throughput: 135.23 ± 2.50
  - Overall Throughput: 5806.27 ± 126.94

#### w8a16_awq_prefill_bound

- **Total runs:** 3

- **Individual runs:**

  - `w8a16_awq_prefill_bound_run1`:
    - Latency: 0.32s
    - Output Throughput: 191.46 tok/s
    - Overall Throughput: 6523.36 tok/s
    - Input Throughput: N/A
  - `w8a16_awq_prefill_bound_run2`:
    - Latency: 0.34s
    - Output Throughput: 170.68 tok/s
    - Overall Throughput: 6120.81 tok/s
    - Input Throughput: N/A
  - `w8a16_awq_prefill_bound_run3`:
    - Latency: 0.35s
    - Output Throughput: 175.85 tok/s
    - Overall Throughput: 5961.15 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.34 ± 0.02
  - Output Throughput: 179.33 ± 10.82
  - Overall Throughput: 6201.77 ± 289.72

#### w8a16_smooth_awq_prefill_bound

- **Total runs:** 3

- **Individual runs:**

  - `w8a16_smooth_awq_prefill_bound_run1`:
    - Latency: 0.34s
    - Output Throughput: 179.85 tok/s
    - Overall Throughput: 6157.39 tok/s
    - Input Throughput: N/A
  - `w8a16_smooth_awq_prefill_bound_run2`:
    - Latency: 0.34s
    - Output Throughput: 170.87 tok/s
    - Overall Throughput: 6120.07 tok/s
    - Input Throughput: N/A
  - `w8a16_smooth_awq_prefill_bound_run3`:
    - Latency: 0.32s
    - Output Throughput: 191.06 tok/s
    - Overall Throughput: 6523.00 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.33 ± 0.01
  - Output Throughput: 180.59 ± 10.12
  - Overall Throughput: 6266.82 ± 222.64

#### w8a16_sparse_awq_prefill_bound

- **Total runs:** 3

- **Individual runs:**

  - `w8a16_sparse_awq_prefill_bound_run1`:
    - Latency: 0.33s
    - Output Throughput: 200.47 tok/s
    - Overall Throughput: 6385.78 tok/s
    - Input Throughput: N/A
  - `w8a16_sparse_awq_prefill_bound_run2`:
    - Latency: 0.32s
    - Output Throughput: 193.28 tok/s
    - Overall Throughput: 6504.51 tok/s
    - Input Throughput: N/A
  - `w8a16_sparse_awq_prefill_bound_run3`:
    - Latency: 0.33s
    - Output Throughput: 184.52 tok/s
    - Overall Throughput: 6364.05 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.32 ± 0.00
  - Output Throughput: 192.76 ± 7.99
  - Overall Throughput: 6418.11 ± 75.61

#### w8a8_smooth_gptq_prefill_bound

- **Total runs:** 3

- **Individual runs:**

  - `w8a8_smooth_gptq_prefill_bound_run1`:
    - Latency: 0.26s
    - Output Throughput: 202.95 tok/s
    - Overall Throughput: 8109.06 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_gptq_prefill_bound_run2`:
    - Latency: 0.29s
    - Output Throughput: 183.04 tok/s
    - Overall Throughput: 7072.57 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_gptq_prefill_bound_run3`:
    - Latency: 0.27s
    - Output Throughput: 189.48 tok/s
    - Overall Throughput: 7799.73 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.27 ± 0.02
  - Output Throughput: 191.82 ± 10.16
  - Overall Throughput: 7660.45 ± 532.10

#### w8a8_smooth_ptq_prefill_bound

- **Total runs:** 3

- **Individual runs:**

  - `w8a8_smooth_ptq_prefill_bound_run1`:
    - Latency: 0.26s
    - Output Throughput: 181.60 tok/s
    - Overall Throughput: 7886.07 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_ptq_prefill_bound_run3`:
    - Latency: 0.27s
    - Output Throughput: 178.05 tok/s
    - Overall Throughput: 7614.76 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_ptq_prefill_bound_run2`:
    - Latency: 0.26s
    - Output Throughput: 179.79 tok/s
    - Overall Throughput: 7861.86 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.27 ± 0.01
  - Output Throughput: 179.81 ± 1.78
  - Overall Throughput: 7787.56 ± 150.14

#### w8a8_sparse_smooth_gptq_prefill_bound

- **Total runs:** 3

- **Individual runs:**

  - `w8a8_sparse_smooth_gptq_prefill_bound_run1`:
    - Latency: 0.28s
    - Output Throughput: 177.75 tok/s
    - Overall Throughput: 7534.41 tok/s
    - Input Throughput: N/A
  - `w8a8_sparse_smooth_gptq_prefill_bound_run3`:
    - Latency: 0.26s
    - Output Throughput: 187.36 tok/s
    - Overall Throughput: 8025.11 tok/s
    - Input Throughput: N/A
  - `w8a8_sparse_smooth_gptq_prefill_bound_run3`:
    - Latency: 0.28s
    - Output Throughput: 170.02 tok/s
    - Overall Throughput: 7303.00 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.27 ± 0.01
  - Output Throughput: 178.38 ± 8.69
  - Overall Throughput: 7620.84 ± 368.73

## Configuration: batch_size=1, input_len=16384, output_len=32

**Total models tested:** 7


### Summary Table

| Model | Runs | Latency (s) | Output Throughput (tok/s) | Overall Throughput (tok/s) | Input Throughput (tok/s) |
|-------|------|-------------|---------------------------|----------------------------|--------------------------|
| `w8a8_sparse_smooth_gptq_long_context` | 3 | 0.99 ± 0.00 | 162.62 ± 1.36 | 16503.84 ± 37.83 | 0.00 |
| `w8a8_smooth_gptq_long_context` | 3 | 0.99 ± 0.01 | 162.43 ± 3.65 | 16505.70 ± 89.21 | 0.00 |
| `w8a8_smooth_ptq_long_context` | 3 | 1.00 ± 0.04 | 160.89 ± 2.67 | 16365.31 ± 664.87 | 0.00 |
| `w8a16_sparse_awq_long_context` | 3 | 1.47 ± 0.01 | 157.46 ± 2.41 | 11131.60 ± 92.82 | 0.00 |
| `w8a16_smooth_awq_long_context` | 3 | 1.48 ± 0.00 | 157.27 ± 1.29 | 11075.30 ± 35.85 | 0.00 |
| `w8a16_awq_long_context` | 3 | 1.48 ± 0.03 | 156.71 ± 0.64 | 11058.47 ± 218.14 | 0.00 |
| `original_long_context` | 3 | 1.24 ± 0.01 | 118.46 ± 2.09 | 13249.45 ± 69.29 | 0.00 |

### Detailed Results


#### original_long_context

- **Total runs:** 3

- **Individual runs:**

  - `original_long_context_run1`:
    - Latency: 1.25s
    - Output Throughput: 116.16 tok/s
    - Overall Throughput: 13180.59 tok/s
    - Input Throughput: N/A
  - `original_long_context_run2`:
    - Latency: 1.24s
    - Output Throughput: 118.97 tok/s
    - Overall Throughput: 13248.61 tok/s
    - Input Throughput: N/A
  - `original_long_context_run3`:
    - Latency: 1.23s
    - Output Throughput: 120.25 tok/s
    - Overall Throughput: 13319.16 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 1.24 ± 0.01
  - Output Throughput: 118.46 ± 2.09
  - Overall Throughput: 13249.45 ± 69.29

#### w8a16_awq_long_context

- **Total runs:** 3

- **Individual runs:**

  - `w8a16_awq_long_context_run1`:
    - Latency: 1.48s
    - Output Throughput: 156.49 tok/s
    - Overall Throughput: 11122.82 tok/s
    - Input Throughput: N/A
  - `w8a16_awq_long_context_run2`:
    - Latency: 1.46s
    - Output Throughput: 156.20 tok/s
    - Overall Throughput: 11237.20 tok/s
    - Input Throughput: N/A
  - `w8a16_awq_long_context_run3`:
    - Latency: 1.52s
    - Output Throughput: 157.43 tok/s
    - Overall Throughput: 10815.39 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 1.48 ± 0.03
  - Output Throughput: 156.71 ± 0.64
  - Overall Throughput: 11058.47 ± 218.14

#### w8a16_smooth_awq_long_context

- **Total runs:** 3

- **Individual runs:**

  - `w8a16_smooth_awq_long_context_run1`:
    - Latency: 1.49s
    - Output Throughput: 157.65 tok/s
    - Overall Throughput: 11033.95 tok/s
    - Input Throughput: N/A
  - `w8a16_smooth_awq_long_context_run2`:
    - Latency: 1.48s
    - Output Throughput: 155.84 tok/s
    - Overall Throughput: 11094.22 tok/s
    - Input Throughput: N/A
  - `w8a16_smooth_awq_long_context_run3`:
    - Latency: 1.48s
    - Output Throughput: 158.33 tok/s
    - Overall Throughput: 11097.73 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 1.48 ± 0.00
  - Output Throughput: 157.27 ± 1.29
  - Overall Throughput: 11075.30 ± 35.85

#### w8a16_sparse_awq_long_context

- **Total runs:** 3

- **Individual runs:**

  - `w8a16_sparse_awq_long_context_run1`:
    - Latency: 1.46s
    - Output Throughput: 155.92 tok/s
    - Overall Throughput: 11211.40 tok/s
    - Input Throughput: N/A
  - `w8a16_sparse_awq_long_context_run3`:
    - Latency: 1.47s
    - Output Throughput: 156.23 tok/s
    - Overall Throughput: 11153.66 tok/s
    - Input Throughput: N/A
  - `w8a16_sparse_awq_long_context_run2`:
    - Latency: 1.49s
    - Output Throughput: 160.24 tok/s
    - Overall Throughput: 11029.73 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 1.47 ± 0.01
  - Output Throughput: 157.46 ± 2.41
  - Overall Throughput: 11131.60 ± 92.82

#### w8a8_smooth_gptq_long_context

- **Total runs:** 3

- **Individual runs:**

  - `w8a8_smooth_gptq_long_context_run1`:
    - Latency: 1.00s
    - Output Throughput: 159.25 tok/s
    - Overall Throughput: 16469.28 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_gptq_long_context_run2`:
    - Latency: 1.00s
    - Output Throughput: 161.63 tok/s
    - Overall Throughput: 16440.47 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_gptq_long_context_run3`:
    - Latency: 0.99s
    - Output Throughput: 166.41 tok/s
    - Overall Throughput: 16607.36 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.99 ± 0.01
  - Output Throughput: 162.43 ± 3.65
  - Overall Throughput: 16505.70 ± 89.21

#### w8a8_smooth_ptq_long_context

- **Total runs:** 3

- **Individual runs:**

  - `w8a8_smooth_ptq_long_context_run1`:
    - Latency: 0.97s
    - Output Throughput: 163.43 tok/s
    - Overall Throughput: 16877.39 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_ptq_long_context_run2`:
    - Latency: 0.99s
    - Output Throughput: 161.14 tok/s
    - Overall Throughput: 16604.64 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_ptq_long_context_run3`:
    - Latency: 1.05s
    - Output Throughput: 158.10 tok/s
    - Overall Throughput: 15613.91 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 1.00 ± 0.04
  - Output Throughput: 160.89 ± 2.67
  - Overall Throughput: 16365.31 ± 664.87

#### w8a8_sparse_smooth_gptq_long_context

- **Total runs:** 3

- **Individual runs:**

  - `w8a8_sparse_smooth_gptq_long_context_run1`:
    - Latency: 1.00s
    - Output Throughput: 164.14 tok/s
    - Overall Throughput: 16485.62 tok/s
    - Input Throughput: N/A
  - `w8a8_sparse_smooth_gptq_long_context_run2`:
    - Latency: 0.99s
    - Output Throughput: 162.18 tok/s
    - Overall Throughput: 16547.34 tok/s
    - Input Throughput: N/A
  - `w8a8_sparse_smooth_gptq_long_context_run3`:
    - Latency: 1.00s
    - Output Throughput: 161.53 tok/s
    - Overall Throughput: 16478.57 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.99 ± 0.00
  - Output Throughput: 162.62 ± 1.36
  - Overall Throughput: 16503.84 ± 37.83

## Configuration: batch_size=8, input_len=256, output_len=128

**Total models tested:** 7


### Summary Table

| Model | Runs | Latency (s) | Output Throughput (tok/s) | Overall Throughput (tok/s) | Input Throughput (tok/s) |
|-------|------|-------------|---------------------------|----------------------------|--------------------------|
| `w8a8_smooth_gptq_medium_batch` | 3 | 0.81 ± 0.02 | 1436.96 ± 24.37 | 3782.56 ± 116.66 | 0.00 |
| `w8a8_sparse_smooth_gptq_medium_batch` | 3 | 0.81 ± 0.01 | 1431.01 ± 18.43 | 3815.86 ± 59.05 | 0.00 |
| `w8a8_smooth_ptq_medium_batch` | 3 | 0.81 ± 0.00 | 1426.83 ± 3.61 | 3813.16 ± 10.09 | 0.00 |
| `w8a16_sparse_awq_medium_batch` | 3 | 0.89 ± 0.01 | 1409.57 ± 27.30 | 3454.81 ± 32.29 | 0.00 |
| `w8a16_awq_medium_batch` | 3 | 0.90 ± 0.03 | 1393.96 ± 20.89 | 3431.93 ± 101.72 | 0.00 |
| `w8a16_smooth_awq_medium_batch` | 3 | 0.90 ± 0.00 | 1368.53 ± 9.68 | 3396.03 ± 15.32 | 0.00 |
| `original_medium_batch` | 3 | 1.07 ± 0.00 | 1072.14 ± 2.26 | 2861.12 ± 11.26 | 0.00 |

### Detailed Results


#### original_medium_batch

- **Total runs:** 3

- **Individual runs:**

  - `original_medium_batch_run1`:
    - Latency: 1.07s
    - Output Throughput: 1072.64 tok/s
    - Overall Throughput: 2867.13 tok/s
    - Input Throughput: N/A
  - `original_medium_batch_run2`:
    - Latency: 1.07s
    - Output Throughput: 1074.11 tok/s
    - Overall Throughput: 2868.10 tok/s
    - Input Throughput: N/A
  - `original_medium_batch_run3`:
    - Latency: 1.08s
    - Output Throughput: 1069.67 tok/s
    - Overall Throughput: 2848.13 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 1.07 ± 0.00
  - Output Throughput: 1072.14 ± 2.26
  - Overall Throughput: 2861.12 ± 11.26

#### w8a16_awq_medium_batch

- **Total runs:** 3

- **Individual runs:**

  - `w8a16_awq_medium_batch_run1`:
    - Latency: 0.87s
    - Output Throughput: 1416.80 tok/s
    - Overall Throughput: 3537.80 tok/s
    - Input Throughput: N/A
  - `w8a16_awq_medium_batch_run2`:
    - Latency: 0.90s
    - Output Throughput: 1375.82 tok/s
    - Overall Throughput: 3423.04 tok/s
    - Input Throughput: N/A
  - `w8a16_awq_medium_batch_run3`:
    - Latency: 0.92s
    - Output Throughput: 1389.26 tok/s
    - Overall Throughput: 3334.95 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.90 ± 0.03
  - Output Throughput: 1393.96 ± 20.89
  - Overall Throughput: 3431.93 ± 101.72

#### w8a16_smooth_awq_medium_batch

- **Total runs:** 3

- **Individual runs:**

  - `w8a16_smooth_awq_medium_batch_run1`:
    - Latency: 0.90s
    - Output Throughput: 1376.55 tok/s
    - Overall Throughput: 3412.84 tok/s
    - Input Throughput: N/A
  - `w8a16_smooth_awq_medium_batch_run2`:
    - Latency: 0.91s
    - Output Throughput: 1357.78 tok/s
    - Overall Throughput: 3392.38 tok/s
    - Input Throughput: N/A
  - `w8a16_smooth_awq_medium_batch_run3`:
    - Latency: 0.91s
    - Output Throughput: 1371.26 tok/s
    - Overall Throughput: 3382.86 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.90 ± 0.00
  - Output Throughput: 1368.53 ± 9.68
  - Overall Throughput: 3396.03 ± 15.32

#### w8a16_sparse_awq_medium_batch

- **Total runs:** 3

- **Individual runs:**

  - `w8a16_sparse_awq_medium_batch_run1`:
    - Latency: 0.88s
    - Output Throughput: 1440.49 tok/s
    - Overall Throughput: 3481.09 tok/s
    - Input Throughput: N/A
  - `w8a16_sparse_awq_medium_batch_run2`:
    - Latency: 0.89s
    - Output Throughput: 1399.43 tok/s
    - Overall Throughput: 3464.57 tok/s
    - Input Throughput: N/A
  - `w8a16_sparse_awq_medium_batch_run3`:
    - Latency: 0.90s
    - Output Throughput: 1388.80 tok/s
    - Overall Throughput: 3418.77 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.89 ± 0.01
  - Output Throughput: 1409.57 ± 27.30
  - Overall Throughput: 3454.81 ± 32.29

#### w8a8_smooth_gptq_medium_batch

- **Total runs:** 3

- **Individual runs:**

  - `w8a8_smooth_gptq_medium_batch_run1`:
    - Latency: 0.81s
    - Output Throughput: 1412.72 tok/s
    - Overall Throughput: 3772.70 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_gptq_medium_batch_run2`:
    - Latency: 0.79s
    - Output Throughput: 1461.45 tok/s
    - Overall Throughput: 3903.84 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_gptq_medium_batch_run3`:
    - Latency: 0.84s
    - Output Throughput: 1436.71 tok/s
    - Overall Throughput: 3671.15 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.81 ± 0.02
  - Output Throughput: 1436.96 ± 24.37
  - Overall Throughput: 3782.56 ± 116.66

#### w8a8_smooth_ptq_medium_batch

- **Total runs:** 3

- **Individual runs:**

  - `w8a8_smooth_ptq_medium_batch_run1`:
    - Latency: 0.81s
    - Output Throughput: 1428.92 tok/s
    - Overall Throughput: 3803.96 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_ptq_medium_batch_run2`:
    - Latency: 0.81s
    - Output Throughput: 1422.67 tok/s
    - Overall Throughput: 3811.57 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_ptq_medium_batch_run3`:
    - Latency: 0.80s
    - Output Throughput: 1428.91 tok/s
    - Overall Throughput: 3823.96 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.81 ± 0.00
  - Output Throughput: 1426.83 ± 3.61
  - Overall Throughput: 3813.16 ± 10.09

#### w8a8_sparse_smooth_gptq_medium_batch

- **Total runs:** 3

- **Individual runs:**

  - `w8a8_sparse_smooth_gptq_medium_batch_run1`:
    - Latency: 0.81s
    - Output Throughput: 1423.77 tok/s
    - Overall Throughput: 3793.47 tok/s
    - Input Throughput: N/A
  - `w8a8_sparse_smooth_gptq_medium_batch_run3`:
    - Latency: 0.81s
    - Output Throughput: 1417.29 tok/s
    - Overall Throughput: 3771.29 tok/s
    - Input Throughput: N/A
  - `w8a8_sparse_smooth_gptq_medium_batch_run3`:
    - Latency: 0.79s
    - Output Throughput: 1451.96 tok/s
    - Overall Throughput: 3882.83 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.81 ± 0.01
  - Output Throughput: 1431.01 ± 18.43
  - Overall Throughput: 3815.86 ± 59.05

## Configuration: batch_size=32, input_len=256, output_len=32

**Total models tested:** 7


### Summary Table

| Model | Runs | Latency (s) | Output Throughput (tok/s) | Overall Throughput (tok/s) | Input Throughput (tok/s) |
|-------|------|-------------|---------------------------|----------------------------|--------------------------|
| `w8a8_smooth_gptq_base` | 3 | 0.46 ± 0.01 | 4800.91 ± 58.75 | 19872.25 ± 406.76 | 0.00 |
| `w8a8_smooth_ptq_base` | 3 | 0.46 ± 0.00 | 4768.20 ± 142.64 | 20078.24 ± 202.74 | 0.00 |
| `w8a8_sparse_smooth_gptq_base` | 3 | 0.45 ± 0.01 | 4249.88 ± 1170.70 | 20452.96 ± 342.84 | 0.00 |
| `w8a16_awq_base` | 3 | 0.74 ± 0.01 | 3993.72 ± 64.07 | 12460.94 ± 229.38 | 0.00 |
| `w8a16_smooth_awq_base` | 3 | 0.75 ± 0.01 | 3963.28 ± 40.92 | 12320.49 ± 204.99 | 0.00 |
| `original_base` | 3 | 0.62 ± 0.02 | 3783.78 ± 25.42 | 14936.69 ± 431.60 | 0.00 |
| `w8a16_sparse_awq_base` | 3 | 0.75 ± 0.00 | 3195.59 ± 1450.51 | 12271.23 ± 43.04 | 0.00 |

### Detailed Results


#### original_base

- **Total runs:** 3

- **Individual runs:**

  - `original_base_run1`:
    - Latency: 0.64s
    - Output Throughput: 3755.92 tok/s
    - Overall Throughput: 14493.95 tok/s
    - Input Throughput: N/A
  - `original_base_run2`:
    - Latency: 0.62s
    - Output Throughput: 3789.70 tok/s
    - Overall Throughput: 14959.91 tok/s
    - Input Throughput: N/A
  - `original_base_run3`:
    - Latency: 0.60s
    - Output Throughput: 3805.71 tok/s
    - Overall Throughput: 15356.21 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.62 ± 0.02
  - Output Throughput: 3783.78 ± 25.42
  - Overall Throughput: 14936.69 ± 431.60

#### w8a16_awq_base

- **Total runs:** 3

- **Individual runs:**

  - `w8a16_awq_base_run1`:
    - Latency: 0.74s
    - Output Throughput: 4048.26 tok/s
    - Overall Throughput: 12392.98 tok/s
    - Input Throughput: N/A
  - `w8a16_awq_base_run2`:
    - Latency: 0.72s
    - Output Throughput: 4009.73 tok/s
    - Overall Throughput: 12716.62 tok/s
    - Input Throughput: N/A
  - `w8a16_awq_base_run3`:
    - Latency: 0.75s
    - Output Throughput: 3923.16 tok/s
    - Overall Throughput: 12273.21 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.74 ± 0.01
  - Output Throughput: 3993.72 ± 64.07
  - Overall Throughput: 12460.94 ± 229.38

#### w8a16_smooth_awq_base

- **Total runs:** 3

- **Individual runs:**

  - `w8a16_smooth_awq_base_run1`:
    - Latency: 0.75s
    - Output Throughput: 3934.09 tok/s
    - Overall Throughput: 12239.88 tok/s
    - Input Throughput: N/A
  - `w8a16_smooth_awq_base_run3`:
    - Latency: 0.76s
    - Output Throughput: 3945.69 tok/s
    - Overall Throughput: 12168.06 tok/s
    - Input Throughput: N/A
  - `w8a16_smooth_awq_base_run3`:
    - Latency: 0.73s
    - Output Throughput: 4010.05 tok/s
    - Overall Throughput: 12553.54 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.75 ± 0.01
  - Output Throughput: 3963.28 ± 40.92
  - Overall Throughput: 12320.49 ± 204.99

#### w8a16_sparse_awq_base

- **Total runs:** 3

- **Individual runs:**

  - `w8a16_sparse_awq_base_run1`:
    - Latency: 0.75s
    - Output Throughput: 1526.74 tok/s
    - Overall Throughput: 12278.80 tok/s
    - Input Throughput: N/A
  - `w8a16_sparse_awq_base_run2`:
    - Latency: 0.75s
    - Output Throughput: 4153.26 tok/s
    - Overall Throughput: 12224.91 tok/s
    - Input Throughput: N/A
  - `w8a16_sparse_awq_base_run3`:
    - Latency: 0.75s
    - Output Throughput: 3906.77 tok/s
    - Overall Throughput: 12309.99 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.75 ± 0.00
  - Output Throughput: 3195.59 ± 1450.51
  - Overall Throughput: 12271.23 ± 43.04

#### w8a8_smooth_gptq_base

- **Total runs:** 3

- **Individual runs:**

  - `w8a8_smooth_gptq_base_run1`:
    - Latency: 0.46s
    - Output Throughput: 4848.36 tok/s
    - Overall Throughput: 20074.63 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_gptq_base_run2`:
    - Latency: 0.47s
    - Output Throughput: 4735.19 tok/s
    - Overall Throughput: 19404.00 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_gptq_base_run3`:
    - Latency: 0.46s
    - Output Throughput: 4819.17 tok/s
    - Overall Throughput: 20138.13 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.46 ± 0.01
  - Output Throughput: 4800.91 ± 58.75
  - Overall Throughput: 19872.25 ± 406.76

#### w8a8_smooth_ptq_base

- **Total runs:** 3

- **Individual runs:**

  - `w8a8_smooth_ptq_base_run1`:
    - Latency: 0.45s
    - Output Throughput: 4932.02 tok/s
    - Overall Throughput: 20301.12 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_ptq_base_run3`:
    - Latency: 0.46s
    - Output Throughput: 4671.46 tok/s
    - Overall Throughput: 20028.84 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_ptq_base_run3`:
    - Latency: 0.46s
    - Output Throughput: 4701.13 tok/s
    - Overall Throughput: 19904.77 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.46 ± 0.00
  - Output Throughput: 4768.20 ± 142.64
  - Overall Throughput: 20078.24 ± 202.74

#### w8a8_sparse_smooth_gptq_base

- **Total runs:** 3

- **Individual runs:**

  - `w8a8_sparse_smooth_gptq_base_run1`:
    - Latency: 0.44s
    - Output Throughput: 4943.59 tok/s
    - Overall Throughput: 20788.91 tok/s
    - Input Throughput: N/A
  - `w8a8_sparse_smooth_gptq_base_run3`:
    - Latency: 0.46s
    - Output Throughput: 2898.23 tok/s
    - Overall Throughput: 20103.63 tok/s
    - Input Throughput: N/A
  - `w8a8_sparse_smooth_gptq_base_run3`:
    - Latency: 0.45s
    - Output Throughput: 4907.82 tok/s
    - Overall Throughput: 20466.35 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 0.45 ± 0.01
  - Output Throughput: 4249.88 ± 1170.70
  - Overall Throughput: 20452.96 ± 342.84

## Configuration: batch_size=64, input_len=256, output_len=128

**Total models tested:** 7


### Summary Table

| Model | Runs | Latency (s) | Output Throughput (tok/s) | Overall Throughput (tok/s) | Input Throughput (tok/s) |
|-------|------|-------------|---------------------------|----------------------------|--------------------------|
| `w8a8_smooth_gptq_high_concurrency` | 3 | 1.52 ± 0.03 | 7581.57 ± 60.26 | 16159.96 ± 346.91 | 0.00 |
| `w8a8_sparse_smooth_gptq_high_concurrency` | 3 | 1.55 ± 0.03 | 7555.92 ± 46.72 | 15903.99 ± 334.92 | 0.00 |
| `w8a8_smooth_ptq_high_concurrency` | 3 | 1.57 ± 0.08 | 7534.97 ± 42.10 | 15701.74 ± 747.29 | 0.00 |
| `original_high_concurrency` | 3 | 1.93 ± 0.01 | 6304.56 ± 24.32 | 12728.15 ± 93.71 | 0.00 |
| `w8a16_awq_high_concurrency` | 3 | 2.48 ± 0.01 | 5244.19 ± 23.09 | 9915.02 ± 44.83 | 0.00 |
| `w8a16_smooth_awq_high_concurrency` | 3 | 2.47 ± 0.01 | 5239.31 ± 11.58 | 9941.34 ± 23.95 | 0.00 |
| `w8a16_sparse_awq_high_concurrency` | 3 | 2.48 ± 0.02 | 5238.97 ± 4.81 | 9908.26 ± 68.79 | 0.00 |

### Detailed Results


#### original_high_concurrency

- **Total runs:** 3

- **Individual runs:**

  - `original_high_concurrency_run1`:
    - Latency: 1.92s
    - Output Throughput: 6293.15 tok/s
    - Overall Throughput: 12799.67 tok/s
    - Input Throughput: N/A
  - `original_high_concurrency_run2`:
    - Latency: 1.93s
    - Output Throughput: 6288.05 tok/s
    - Overall Throughput: 12762.71 tok/s
    - Input Throughput: N/A
  - `original_high_concurrency_run3`:
    - Latency: 1.95s
    - Output Throughput: 6332.49 tok/s
    - Overall Throughput: 12622.06 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 1.93 ± 0.01
  - Output Throughput: 6304.56 ± 24.32
  - Overall Throughput: 12728.15 ± 93.71

#### w8a16_awq_high_concurrency

- **Total runs:** 3

- **Individual runs:**

  - `w8a16_awq_high_concurrency_run1`:
    - Latency: 2.48s
    - Output Throughput: 5270.77 tok/s
    - Overall Throughput: 9905.37 tok/s
    - Input Throughput: N/A
  - `w8a16_awq_high_concurrency_run2`:
    - Latency: 2.49s
    - Output Throughput: 5229.00 tok/s
    - Overall Throughput: 9875.80 tok/s
    - Input Throughput: N/A
  - `w8a16_awq_high_concurrency_run3`:
    - Latency: 2.47s
    - Output Throughput: 5232.81 tok/s
    - Overall Throughput: 9963.89 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 2.48 ± 0.01
  - Output Throughput: 5244.19 ± 23.09
  - Overall Throughput: 9915.02 ± 44.83

#### w8a16_smooth_awq_high_concurrency

- **Total runs:** 3

- **Individual runs:**

  - `w8a16_smooth_awq_high_concurrency_run1`:
    - Latency: 2.48s
    - Output Throughput: 5250.41 tok/s
    - Overall Throughput: 9916.86 tok/s
    - Input Throughput: N/A
  - `w8a16_smooth_awq_high_concurrency_run2`:
    - Latency: 2.47s
    - Output Throughput: 5240.23 tok/s
    - Overall Throughput: 9964.72 tok/s
    - Input Throughput: N/A
  - `w8a16_smooth_awq_high_concurrency_run3`:
    - Latency: 2.47s
    - Output Throughput: 5227.30 tok/s
    - Overall Throughput: 9942.45 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 2.47 ± 0.01
  - Output Throughput: 5239.31 ± 11.58
  - Overall Throughput: 9941.34 ± 23.95

#### w8a16_sparse_awq_high_concurrency

- **Total runs:** 3

- **Individual runs:**

  - `w8a16_sparse_awq_high_concurrency_run1`:
    - Latency: 2.48s
    - Output Throughput: 5233.53 tok/s
    - Overall Throughput: 9928.96 tok/s
    - Input Throughput: N/A
  - `w8a16_sparse_awq_high_concurrency_run2`:
    - Latency: 2.50s
    - Output Throughput: 5242.67 tok/s
    - Overall Throughput: 9831.50 tok/s
    - Input Throughput: N/A
  - `w8a16_sparse_awq_high_concurrency_run3`:
    - Latency: 2.47s
    - Output Throughput: 5240.72 tok/s
    - Overall Throughput: 9964.32 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 2.48 ± 0.02
  - Output Throughput: 5238.97 ± 4.81
  - Overall Throughput: 9908.26 ± 68.79

#### w8a8_smooth_gptq_high_concurrency

- **Total runs:** 3

- **Individual runs:**

  - `w8a8_smooth_gptq_high_concurrency_run1`:
    - Latency: 1.49s
    - Output Throughput: 7625.43 tok/s
    - Overall Throughput: 16504.60 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_gptq_high_concurrency_run2`:
    - Latency: 1.55s
    - Output Throughput: 7512.86 tok/s
    - Overall Throughput: 15810.83 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_gptq_high_concurrency_run3`:
    - Latency: 1.52s
    - Output Throughput: 7606.42 tok/s
    - Overall Throughput: 16164.46 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 1.52 ± 0.03
  - Output Throughput: 7581.57 ± 60.26
  - Overall Throughput: 16159.96 ± 346.91

#### w8a8_smooth_ptq_high_concurrency

- **Total runs:** 3

- **Individual runs:**

  - `w8a8_smooth_ptq_high_concurrency_run1`:
    - Latency: 1.53s
    - Output Throughput: 7552.76 tok/s
    - Overall Throughput: 16099.32 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_ptq_high_concurrency_run2`:
    - Latency: 1.52s
    - Output Throughput: 7565.26 tok/s
    - Overall Throughput: 16166.19 tok/s
    - Input Throughput: N/A
  - `w8a8_smooth_ptq_high_concurrency_run3`:
    - Latency: 1.66s
    - Output Throughput: 7486.89 tok/s
    - Overall Throughput: 14839.70 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 1.57 ± 0.08
  - Output Throughput: 7534.97 ± 42.10
  - Overall Throughput: 15701.74 ± 747.29

#### w8a8_sparse_smooth_gptq_high_concurrency

- **Total runs:** 3

- **Individual runs:**

  - `w8a8_sparse_smooth_gptq_high_concurrency_run1`:
    - Latency: 1.52s
    - Output Throughput: 7551.90 tok/s
    - Overall Throughput: 16131.20 tok/s
    - Input Throughput: N/A
  - `w8a8_sparse_smooth_gptq_high_concurrency_run2`:
    - Latency: 1.58s
    - Output Throughput: 7604.52 tok/s
    - Overall Throughput: 15519.37 tok/s
    - Input Throughput: N/A
  - `w8a8_sparse_smooth_gptq_high_concurrency_run3`:
    - Latency: 1.53s
    - Output Throughput: 7511.33 tok/s
    - Overall Throughput: 16061.41 tok/s
    - Input Throughput: N/A
- **Statistics:**

  - Latency: 1.55 ± 0.03
  - Output Throughput: 7555.92 ± 46.72
  - Overall Throughput: 15903.99 ± 334.92

---


## Performance Ranking (by Output Throughput)


### Configuration: batch_size=1, input_len=128, output_len=64

🥇 **w8a8_sparse_smooth_gptq_interactive**: 193.82 tok/s
🥈 **w8a8_smooth_gptq_interactive**: 192.33 tok/s
🥉 **w8a8_smooth_ptq_interactive**: 191.32 tok/s
4. **w8a16_sparse_awq_interactive**: 181.78 tok/s
5. **w8a16_smooth_awq_interactive**: 180.34 tok/s
6. **w8a16_awq_interactive**: 177.93 tok/s
7. **original_interactive**: 132.75 tok/s

### Configuration: batch_size=1, input_len=256, output_len=512

🥇 **w8a8_sparse_smooth_gptq_decode_bound**: 198.06 tok/s
🥈 **w8a8_smooth_ptq_decode_bound**: 197.63 tok/s
🥉 **w8a8_smooth_gptq_decode_bound**: 197.20 tok/s
4. **w8a16_sparse_awq_decode_bound**: 188.21 tok/s
5. **w8a16_awq_decode_bound**: 187.49 tok/s
6. **w8a16_smooth_awq_decode_bound**: 187.18 tok/s
7. **original_decode_bound**: 136.47 tok/s

### Configuration: batch_size=1, input_len=2048, output_len=32

🥇 **w8a16_sparse_awq_prefill_bound**: 192.76 tok/s
🥈 **w8a8_smooth_gptq_prefill_bound**: 191.82 tok/s
🥉 **w8a16_smooth_awq_prefill_bound**: 180.59 tok/s
4. **w8a8_smooth_ptq_prefill_bound**: 179.81 tok/s
5. **w8a16_awq_prefill_bound**: 179.33 tok/s
6. **w8a8_sparse_smooth_gptq_prefill_bound**: 178.38 tok/s
7. **original_prefill_bound**: 135.23 tok/s

### Configuration: batch_size=1, input_len=16384, output_len=32

🥇 **w8a8_sparse_smooth_gptq_long_context**: 162.62 tok/s
🥈 **w8a8_smooth_gptq_long_context**: 162.43 tok/s
🥉 **w8a8_smooth_ptq_long_context**: 160.89 tok/s
4. **w8a16_sparse_awq_long_context**: 157.46 tok/s
5. **w8a16_smooth_awq_long_context**: 157.27 tok/s
6. **w8a16_awq_long_context**: 156.71 tok/s
7. **original_long_context**: 118.46 tok/s

### Configuration: batch_size=8, input_len=256, output_len=128

🥇 **w8a8_smooth_gptq_medium_batch**: 1436.96 tok/s
🥈 **w8a8_sparse_smooth_gptq_medium_batch**: 1431.01 tok/s
🥉 **w8a8_smooth_ptq_medium_batch**: 1426.83 tok/s
4. **w8a16_sparse_awq_medium_batch**: 1409.57 tok/s
5. **w8a16_awq_medium_batch**: 1393.96 tok/s
6. **w8a16_smooth_awq_medium_batch**: 1368.53 tok/s
7. **original_medium_batch**: 1072.14 tok/s

### Configuration: batch_size=32, input_len=256, output_len=32

🥇 **w8a8_smooth_gptq_base**: 4800.91 tok/s
🥈 **w8a8_smooth_ptq_base**: 4768.20 tok/s
🥉 **w8a8_sparse_smooth_gptq_base**: 4249.88 tok/s
4. **w8a16_awq_base**: 3993.72 tok/s
5. **w8a16_smooth_awq_base**: 3963.28 tok/s
6. **original_base**: 3783.78 tok/s
7. **w8a16_sparse_awq_base**: 3195.59 tok/s

### Configuration: batch_size=64, input_len=256, output_len=128

🥇 **w8a8_smooth_gptq_high_concurrency**: 7581.57 tok/s
🥈 **w8a8_sparse_smooth_gptq_high_concurrency**: 7555.92 tok/s
🥉 **w8a8_smooth_ptq_high_concurrency**: 7534.97 tok/s
4. **original_high_concurrency**: 6304.56 tok/s
5. **w8a16_awq_high_concurrency**: 5244.19 tok/s
6. **w8a16_smooth_awq_high_concurrency**: 5239.31 tok/s
7. **w8a16_sparse_awq_high_concurrency**: 5238.97 tok/s