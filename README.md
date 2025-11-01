# Qwen3-4B-Instruct INT8 Quantization and Evaluation

Comprehensive INT8 quantization, deployment, and evaluation framework for Qwen3-4B-Instruct-2507 model.

---

## 📋 Purpose

This project implements and evaluates multiple INT8 quantization methods (W8A16, W8A8) for Qwen3-4B-Instruct, including:

- **Quantization**: W8A16/W8A8 using SmoothQuant, GPTQ, AWQ, SparseGPT
- **Performance Benchmarking**: Throughput and latency testing with sglang
- **Quality Evaluation**: GPQA accuracy assessment
- **Comprehensive Analysis**: Performance vs. accuracy trade-offs across 7 configurations

---

## 📁 Project Structure

```
qwen_quantization/
├── quantization/           # Quantization scripts
│   └── quantize_model.py
├── scripts/                # Parallel execution scripts
│   ├── parallel_eval.py
│   ├── run_parallel_eval.sh
│   └── run_parallel_quantize.sh
├── performance/            # Performance testing and analysis
│   ├── run_benchmark.py
│   ├── visualize_results.py
│   └── generate_summary_report.py
├── simple_evals/           # Evaluation framework (fork)
├── run_gpqa_sglang.py      # GPQA evaluation script
├── system_info.md          # System configuration
└── README.md
```

---

## 🚀 Quick Start

### 1. Quantize Model

```bash
# Activate environment
source venv/bin/activate

# Run quantization (30-60 minutes)
python quantization/quantize_model.py --method w8a8_smooth_gptq
```

### 2. Performance Benchmarking

```bash
# Start server
python -m sglang.launch_server --model-path <MODEL_PATH> --port 30000

# Run benchmark
python -m sglang.bench_one_batch_server \
  --base-url http://127.0.0.1:30000 \
  --model-path <MODEL_PATH> \
  --batch-size 32 --input-len 256 --output-len 32
```

### 3. GPQA Evaluation

```bash
# Quick test (3 questions)
python run_gpqa_sglang.py --model original --num-examples 3

# Full evaluation (diamond, 50 repeats, greedy)
python run_gpqa_sglang.py --model original --variant diamond --n-repeats 50 --greedy
```

---

## 💻 System Environment

### Hardware
- **GPU**: NVIDIA A100-SXM4-80GB × 8
- **CPU**: Intel Xeon Platinum 8480+ (224 cores)
- **Memory**: 2.0 TB
- **CUDA**: 12.1

### Key Dependencies
- `torch==2.8.0` (CUDA 12.1)
- `transformers==4.57.1`
- `sglang==0.5.3.post3`
- `llmcompressor==0.8.1`
- `vllm==0.11.0`

---

## 📚 References

- [llmcompressor Documentation](https://github.com/vllm-project/llm-compressor)
- [sglang Documentation](https://docs.sglang.ai/)
- [OpenAI Simple Evals](https://github.com/openai/simple-evals)
- [GPQA Paper](https://arxiv.org/abs/2311.12022)
- [Qwen3 Model](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507)

---

**For detailed configuration and advanced usage, see `system_info.md`.**
