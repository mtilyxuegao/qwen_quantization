# Qwen3-4B-Instruct INT8 量化与评估

本项目完成 Qwen3-4B-Instruct-2507 模型的 INT8 量化、部署和质量评估。

## 📁 项目结构

```
qwen_quantization/
├── scripts/
│   └── quantize_model.py       # 模型量化脚本
├── run_gpqa_eval.py            # GPQA 评估脚本
├── simple-evals/               # OpenAI simple-evals 仓库
├── results/                    # 评估结果输出目录
├── system_info.md              # 系统配置信息
└── README.md                   # 本文件
```

## 🚀 快速开始

```bash
# 1. 量化模型
python scripts/quantize_model.py

# 2. 启动 sglang（原始模型）
python -m sglang.launch_server --model-path <模型路径> --port 30000

# 3. 测试评估（10题）
python run_gpqa_eval.py --model-name test --num-examples 10

# 4. 完整评估
python run_gpqa_eval.py --model-name qwen3-4b-original
```

---

## 📖 完整流程

### 阶段 1: 模型量化

使用 llmcompressor 将模型量化为 INT8 (W8A8)。

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行量化脚本（需要 30-60 分钟）
python scripts/quantize_model.py
```

**量化配置：**
- 算法: SmoothQuant + GPTQ
- 方案: W8A8 (权重和激活均为 INT8)
- 校准数据: ultrachat_200k (512 样本)
- 输出路径: `/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A8`

---

### 阶段 2: 部署推理服务

使用 sglang 部署模型（支持 OpenAI 兼容 API）。

#### 原始模型

```bash
python -m sglang.launch_server \
  --model-path /data/jisenli2/huggingface/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/cdbee75f17c01a7cc42f958dc650907174af0554 \
  --host 0.0.0.0 \
  --port 30000 \
  --context-length 262144
```

#### INT8 量化模型

```bash
python -m sglang.launch_server \
  --model-path /data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A8 \
  --host 0.0.0.0 \
  --port 30000 \
  --context-length 262144
```

**服务端点：** `http://127.0.0.1:30000/v1` (OpenAI 兼容)

---

### 阶段 3: 速度评估

使用 sglang 自带的 benchmark 工具测试吞吐量。

```bash
python -m sglang.bench_one_batch_server \
  --base-url http://127.0.0.1:30000 \
  --model-path Qwen/Qwen3-4B-Instruct-2507 \
  --batch-size 32 \
  --input-len 256 \
  --output-len 32
```

记录以下指标：
- **Throughput** (tokens/s)
- **Latency** (ms)
- **GPU Memory** (GB)

---

### 阶段 4: 质量评估 (GPQA)

使用 OpenAI Simple Evals 的 GPQA benchmark 测试模型准确率。

#### 评估原始模型

```bash
# 确保 sglang 服务器已启动（原始模型）

# 完整评估（448题×10次）
python run_gpqa_eval.py --model-name qwen3-4b-original

# 测试模式（10题×10次）
python run_gpqa_eval.py --model-name qwen3-4b-original --num-examples 10
```

#### 评估 INT8 模型

```bash
# 停止原始模型服务器，启动 INT8 模型服务器

# 运行评估
python run_gpqa_eval.py --model-name qwen3-4b-int8
```

#### 命令行参数

```bash
--model-name     模型名称（用于保存结果）
--base-url       sglang 服务器地址（默认: http://127.0.0.1:30000/v1）
--num-examples   限制测试样本数（None=全部）
--n-repeats      重复评估次数（默认: 10）
--variant        GPQA 变体（默认: diamond）
--seed           随机种子起始值（默认: 1234）
--max-tokens     最大输出长度（默认: 4096）
--output-dir     结果保存目录（默认: results/）
```

**GPQA 说明：**
- Diamond 变体：448 道研究生级别科学问答题
- 重复评估：外层循环 10 次，每次独立评估所有题目
- 预计耗时：每次约 1 小时，总计 10 小时
- 建议先用 `--num-examples 10 --n-repeats 1` 快速测试
- **增量保存**：每完成一遍（repeat）立即保存，可查看中间进度

---

## 📊 评估参数

### 采样参数（硬编码）
- Temperature: 0.7
- Top-P: 0.8
- Top-K: 20
- Min-P: 0.0
- Max Tokens: 4096（可通过 `--max-tokens` 修改）

### GPQA 配置
- n_repeats: 10（外层循环次数）
- variant: diamond（可选：diamond, extended, main）
- num_examples: None（全部448题）
- seed: 1234（每次查询自动递增）

---

## 📈 结果文件

评估完成后在 `results/` 目录生成：

- `gpqa_{model}_repeat0.json` - 第1次评估结果
- `gpqa_{model}_repeat1.json` - 第2次评估结果
- ...
- `gpqa_{model}_repeat9.json` - 第10次评估结果
- `gpqa_{model}_final.json` - 汇总统计（均值、标准差）
- `gpqa_{model}.html` - HTML 报告

### 指标对比

```python
# 读取汇总结果
import json

with open('results/gpqa_qwen3-4b-original_final.json') as f:
    original = json.load(f)
    
with open('results/gpqa_qwen3-4b-int8_final.json') as f:
    int8 = json.load(f)

print(f"原始模型: {original['mean_score']:.4f} ± {original['std_score']:.4f}")
print(f"INT8 模型: {int8['mean_score']:.4f} ± {int8['std_score']:.4f}")
print(f"准确率下降: {(original['mean_score'] - int8['mean_score']):.4f}")
```

---

## 🖥️ 系统环境

- **GPU**: NVIDIA A100 80GB × 8 (使用 1 个)
- **CPU**: Intel Xeon Platinum 8480+ (224 核)
- **内存**: 2.0 TB
- **CUDA**: 12.1
- **Python**: 3.10.12

### 关键依赖
- llmcompressor==0.8.1
- vllm==0.11.0
- sglang==0.5.3.post3
- torch==2.8.0
- transformers==4.57.1

---

## ⚠️ 注意事项

1. **量化**: 首次量化约 30-60 分钟，会下载 ultrachat 数据集（~1-2GB）

2. **显存**:
   - 原始模型: ~8-10GB
   - INT8 模型: ~4-6GB
   - 量化过程: ~15-20GB

3. **评估**: 完整评估需 1-2 小时，建议先用 `--num-examples 10` 测试

4. **增量保存**: 
   - 每完成一遍（repeat）立即保存到 `*_repeat{n}.json`
   - 中断后已完成的 repeats 结果保留
   - 可随时查看中间进度和统计

5. **依赖冲突**: 如遇 llmcompressor 错误：
   ```bash
   pip install --upgrade compressed-tensors datasets
   ```

---

## 📚 参考资料

- [vLLM INT8 量化文档](https://docs.vllm.ai/en/latest/features/quantization/int8.html)
- [sglang 文档](https://docs.sglang.ai/)
- [OpenAI Simple Evals](https://github.com/openai/simple-evals)
- [GPQA 论文](https://arxiv.org/abs/2311.12022)
- [Qwen3 模型](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507)
