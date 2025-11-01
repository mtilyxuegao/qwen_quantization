# System Information

## Hardware Configuration

### GPU Information

**GPU Model:** NVIDIA A100-SXM4-80GB
**Memory Capacity:** 80GB (81920 MiB)
**GPU Count:** 8 available (**Experiment usage: 1 GPU per task**)

**Driver and Runtime:**
- **NVIDIA Driver:** 565.57.01
- **CUDA Version:** 12.1
- **cuDNN Version:** 9.1.2 (build 91002)
- **PyTorch CUDA:** Enabled (CUDA 12.1)
- **cuDNN Support:** Enabled
- nvcc: Not installed in user space (HPC environment limitation)

---

### CPU and Memory Information

**CPU Model:** Intel(R) Xeon(R) Platinum 8480+
**Total Cores:** 224 cores (server node)
**Experiment Usage:** 64 cores

**Memory Configuration:**
- **Total Memory:** 2.0 TB (server node)
- **Experiment Usage:** ~439 GB
- **Swap:** 0 GB (not configured)

---

## Software Environment

### Operating System
- **System:** Ubuntu 22.04.5 LTS
- **Kernel Version:** 5.15.0-140-generic
- **Shell:** /bin/bash

### Python Environment
- **Python Version:** 3.10.12
- **Virtual Environment:** venv (located at /home/jisenli2/qwen_quantization/venv)

### Key Dependencies

| Package | Version | Description |
|---------|---------|-------------|
| **torch** | **2.8.0** | **PyTorch Deep Learning Framework (CUDA 12.1)** |
| **transformers** | **4.57.1** | **Hugging Face Transformers** |
| **sglang** | **0.5.3.post3** | **Performance Testing Framework** |
| **llmcompressor** | **0.8.1** | **Model Quantization Tool** |
| vllm | 0.11.0 | LLM Inference Engine |
| torchao | 0.9.0 | PyTorch Quantization Acceleration Library |
| torchaudio | 2.8.0 | PyTorch Audio Processing |
| torchvision | 0.23.0 | PyTorch Vision Processing |

**PyTorch Configuration:**
- CUDA Version: 12.1
- CUDA Available: ✅ Yes
- cuDNN Enabled: ✅ Yes
- cuDNN Version: 9.1.2

---

## HPC Environment Information

- **Working Directory:** /home/jisenli2/qwen_quantization
- **Username:** jisenli2
- **Node Name:** research-external-05
- **Available GPU:** NVIDIA A100 80GB (allocated to current node)
- **Shared Storage:** /data/shared/huggingface/ (team shared model storage)

---

## Storage Space

**Storage Status:**
- `/home` partition: 9.7TB total, 8.1TB used, 1.2TB available (88% usage)
- `/data` partition: 9.8TB total, 8.4TB used, 1.4TB available (86% usage)

**Estimated Storage Requirements:**
- Original model (Qwen3-4B-Instruct-2507): ~8 GB
- INT8 quantized model: ~4-5 GB
- Evaluation datasets and logs: ~1-2 GB
- **Total:** ~15 GB

**Download Target:** Use /data partition to store models (more space available)

---

## Network Configuration

**Hugging Face Configuration:**
- Download target path: `/data/jisenli2/huggingface/`
- Local cache: `~/.cache/huggingface/hub/`
- Shared model library: `/data/shared/huggingface/hub/`

**Target Model:**
- Qwen/Qwen3-4B-Instruct-2507 (needs download)

---

## Evaluation Framework and Configuration

### Evaluation Framework
- **Framework:** simple-evals (fork from OpenAI simple-evals)
- **Repository:** https://github.com/mtilyxuegao/simple-evals.git
- **Branch:** gpqa
- **Commit:** ec4f0b1
- **Last Update:** 2025-10-26 15:44:37 -0700

### Random Seed Configuration
Fixed random seeds are used during evaluation to ensure reproducibility:

| Evaluation Task | Random Seed | Purpose |
|----------------|-------------|---------|
| GPQA | `Random(0)` | Option order randomization |
| GPQA Few-shot | `Random(42)` | Few-shot example sampling |

**Note:** All random seeds are fixed to ensure fully reproducible results across runs.

---

## Experiment Resource Configuration

### Compute Node Configuration
Experiments run on a single compute node with the following configuration:
- **GPU:** 8 × NVIDIA A100-80GB
- **CPU:** 64 cores
- **Memory:** ~439 GB
- **Scheduling System:** SLURM (HPC cluster)

### Resource Usage Strategy
- **Per Task Usage:** 1 GPU (independent execution)
- **Parallel Capacity:** Up to 8 tasks running simultaneously
- **Typical Scenarios:**
  - Quantization: 1 GPU, sequential execution
  - Evaluation: Up to 8 GPUs in parallel, testing different models
  - Performance Testing: Up to 8 GPUs in parallel, testing different models

---

## Date and Time

- **Collection Date:** 2025-11-01
- **System Deployment:** 2025-10-18
- **Last Update:** 2025-11-01


